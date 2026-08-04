import { defineStore } from "pinia";
import api from "../services/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: localStorage.getItem("access_token") || null,
    user: JSON.parse(localStorage.getItem("user") || "null"),
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    permissionCodes: (state) => state.user?.role?.permissions || [],
  },

  actions: {
    hasPermission(code) {
      return this.user?.is_superuser || this.permissionCodes.includes(code);
    },

    async login(email, password) {
      const { data } = await api.post("/accounts/login/", { email, password });
      this.accessToken = data.access;
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      await this.fetchMe();
    },

    async fetchMe() {
      const { data } = await api.get("/accounts/me/");
      this.user = data;
      localStorage.setItem("user", JSON.stringify(data));
    },

    logout() {
      this.accessToken = null;
      this.user = null;
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user");
    },
  },
});
