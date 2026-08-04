import api from "./api";

export default {
  listAnnouncements: () => api.get("/content/announcements/"),
  createAnnouncement: (data) => api.post("/content/announcements/", data),
  updateAnnouncement: (id, data) => api.put(`/content/announcements/${id}/`, data),
  removeAnnouncement: (id) => api.delete(`/content/announcements/${id}/`),
};
