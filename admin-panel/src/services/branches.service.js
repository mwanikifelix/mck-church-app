import api from "./api";

export default {
  list: () => api.get("/accounts/branches/"),
  create: (data) => api.post("/accounts/branches/", data),
};
