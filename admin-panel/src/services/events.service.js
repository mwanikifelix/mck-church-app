import api from "./api";

export default {
  list: () => api.get("/events/"),
  get: (id) => api.get(`/events/${id}/`),
  create: (data) => api.post("/events/", data),
  update: (id, data) => api.put(`/events/${id}/`, data),
  remove: (id) => api.delete(`/events/${id}/`),
  rsvp: (id, status) => api.post(`/events/${id}/rsvp/`, { status }),
  attendees: (id) => api.get(`/events/${id}/attendees/`),
};
