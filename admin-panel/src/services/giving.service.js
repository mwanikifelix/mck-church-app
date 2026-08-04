import api from "./api";

export default {
  listDonations: (params) => api.get("/giving/donations/", { params }),
  myDonations: () => api.get("/giving/donations/mine/"),
  getPaybill: () => api.get("/giving/paybill/"),
};
