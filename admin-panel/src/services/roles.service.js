import api from "./api";

export default {
  listRoles: () => api.get("/accounts/roles/"),
  getRole: (id) => api.get(`/accounts/roles/${id}/`),
  setPermissions: (id, codes) => api.patch(`/accounts/roles/${id}/permissions/`, { codes }),
  listPermissions: () => api.get("/accounts/permissions/"),
};
