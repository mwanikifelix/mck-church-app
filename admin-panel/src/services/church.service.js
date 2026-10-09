import api from "./api";

export default {
  listDepartments: () => api.get("/church/departments/"),
  createDepartment: (data) => api.post("/church/departments/", data),
  getDepartment: (id) => api.get(`/church/departments/${id}/`),
  listLeadership: () => api.get("/church/leadership/"),
  listDepartmentMembers: (deptId) => api.get("/church/department-members/", { params: { department: deptId } }),
  listJoinRequests: (params) => api.get("/church/join-requests/", { params }),
  approveJoinRequest: (id) => api.post(`/church/join-requests/${id}/approve/`),
  rejectJoinRequest: (id) => api.post(`/church/join-requests/${id}/reject/`),
};
