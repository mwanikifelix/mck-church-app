import api from "./api";

export default {
  listCounselling: () => api.get("/pastoral/counselling/"),
  updateCounselling: (id, data) => api.patch(`/pastoral/counselling/${id}/`, data),
  listClergy: () => api.get("/pastoral/clergy/"),
};
