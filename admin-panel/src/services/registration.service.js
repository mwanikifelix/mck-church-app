import api from "./api";

export default {
  listWindows: () => api.get("/registration/windows/"),
  createWindow: (data) => api.post("/registration/windows/", data),

  listCatechism: (params) => api.get("/registration/catechism/", { params }),
};
