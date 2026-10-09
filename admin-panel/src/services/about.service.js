import api from "./api";

export default {
  listGallery: () => api.get("/about/gallery/"),
  uploadPhoto: (formData) =>
    api.post("/about/gallery/", formData, { headers: { "Content-Type": "multipart/form-data" } }),
  deletePhoto: (id) => api.delete(`/about/gallery/${id}/`),

  listFacilities: () => api.get("/about/facilities/"),
  createFacility: (data) => api.post("/about/facilities/", data),

  listSchedule: () => api.get("/about/service-schedule/"),
  createScheduleRow: (data) => api.post("/about/service-schedule/", data),
};
