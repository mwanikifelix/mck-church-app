import api from "./api";

export default {
  list: (params) => api.get("/accounts/members/", { params }),
  create: (data) => api.post("/accounts/signup/", data),
  get: (id) => api.get(`/accounts/members/${id}/`),
};
