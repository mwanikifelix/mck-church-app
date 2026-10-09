import api from "./api";

export default {
  list: () => api.get("/hbc/"),
  create: (data) => api.post("/hbc/", data),
  get: (id) => api.get(`/hbc/${id}/`),
  mine: () => api.get("/hbc/mine/"),
  join: (id) => api.post(`/hbc/${id}/join/`),
  contributions: (id) => api.get(`/hbc/${id}/contributions/`),
  posts: (id) => api.get(`/hbc/${id}/posts/`),
};
