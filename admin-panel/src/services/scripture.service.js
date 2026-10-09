import api from "./api";

export default {
  listVersions: () => api.get("/scripture/bible/versions/"),
  createVersion: (data) => api.post("/scripture/bible/versions/", data),

  listHymns: () => api.get("/scripture/hymns/"),
  createHymn: (data) => api.post("/scripture/hymns/", data),

  createHymnFile: (formData) =>
    api.post("/scripture/hymn-files/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),
};
