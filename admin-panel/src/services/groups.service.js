import api from "./api";

export default {
  list: () => api.get("/groups/groups/"),
  get: (id) => api.get(`/groups/groups/${id}/`),
  create: (data) => api.post("/groups/groups/", data),
  update: (id, data) => api.put(`/groups/groups/${id}/`, data),
  remove: (id) => api.delete(`/groups/groups/${id}/`),
  members: (id) => api.get(`/groups/groups/${id}/members/`),
  join: (id) => api.post(`/groups/groups/${id}/join/`),
  stages: () => api.get("/groups/stages/"),
  memberships: () => api.get("/groups/memberships/"),
  graduations: () => api.get("/groups/graduations/"),
  graduate: (data) => api.post("/groups/graduations/graduate/", data),
};
