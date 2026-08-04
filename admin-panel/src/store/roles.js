import { defineStore } from "pinia";
import rolesService from "../services/roles.service";

export const useRolesStore = defineStore("roles", {
  state: () => ({
    roles: [],
    permissions: [],
    loading: false,
  }),
  actions: {
    async fetchAll() {
      this.loading = true;
      try {
        const [rolesRes, permsRes] = await Promise.all([
          rolesService.listRoles(),
          rolesService.listPermissions(),
        ]);
        this.roles = rolesRes.data.results || rolesRes.data;
        this.permissions = permsRes.data.results || permsRes.data;
      } finally {
        this.loading = false;
      }
    },
  },
});
