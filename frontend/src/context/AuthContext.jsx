import { createContext, useContext, useState, useEffect, useCallback } from "react";
import { authApi } from "../api/auth";
import apiClient from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const setAuthHeader = (token) => {
    if (token) {
      apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    } else {
      delete apiClient.defaults.headers.common["Authorization"];
    }
  };

  useEffect(() => {
    // Try to restore token from localStorage as fallback
    const savedToken = localStorage.getItem("access_token");
    if (savedToken) setAuthHeader(savedToken);

    authApi.getMe()
      .then((res) => setUser(res.data))
      .catch(() => {
        setUser(null);
        localStorage.removeItem("access_token");
        setAuthHeader(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (email, password) => {
    const res = await authApi.login({ email, password });
    const token = res.data.access_token;
    // Store token in localStorage as fallback for cross-origin cookie issues
    localStorage.setItem("access_token", token);
    setAuthHeader(token);
    setUser(res.data.user);
    return res.data;
  }, []);

  const logout = useCallback(async () => {
    await authApi.logout();
    localStorage.removeItem("access_token");
    setAuthHeader(null);
    setUser(null);
  }, []);

  const register = useCallback(async (data) => {
    const res = await authApi.register(data);
    return res.data;
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
