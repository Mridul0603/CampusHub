import apiClient from "./client";

export const noticesApi = {
  getAll: (params) => apiClient.get("/api/notices", { params }),
  getById: (id) => apiClient.get(`/api/notices/${id}`),
  create: (data) => apiClient.post("/api/notices", data),
  update: (id, data) => apiClient.put(`/api/notices/${id}`, data),
  delete: (id) => apiClient.delete(`/api/notices/${id}`),
  summarize: (id) => apiClient.post(`/api/notices/${id}/summarize`),
};
