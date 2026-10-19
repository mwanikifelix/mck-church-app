import api from "./api";

// Singleton church profile — served by apps.membership.ChurchProfile
// (`GET/PUT /api/membership/church-profile/`). One row exists for the whole
// church; the About page's "Church Profile" tab reads and writes it.
export default {
  get: () => api.get("/membership/church-profile/"),
  update: (data) => api.put("/membership/church-profile/", data),
};
