import api from "./api";

export default {
  list: () => api.get("/prayer/"),
  support: (id) => api.post(`/prayer/${id}/support/`),
  markAnswered: (id) => api.post(`/prayer/${id}/mark_answered/`),
};
