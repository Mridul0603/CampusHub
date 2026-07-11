import apiClient from "./client";

export const placementApi = {
  getAll: (params) => apiClient.get("/api/placement/applications", { params }),
  create: (data) => apiClient.post("/api/placement/applications", data),
  update: (id, data) => apiClient.put(`/api/placement/applications/${id}`, data),
  delete: (id) => apiClient.delete(`/api/placement/applications/${id}`),
  getStats: () => apiClient.get("/api/placement/stats"),
};
