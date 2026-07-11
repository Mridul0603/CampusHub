import apiClient from "./client";

export const authApi = {
  register: (data) => apiClient.post("/api/auth/register", data),
  login: (data) => apiClient.post("/api/auth/login", data),
  logout: () => apiClient.post("/api/auth/logout"),
  getMe: () => apiClient.get("/api/auth/me"),
  forgotPassword: (email) => apiClient.post("/api/auth/forgot-password", { email }),
  resetPassword: (token, new_password) =>
    apiClient.post("/api/auth/reset-password", { token, new_password }),
};
