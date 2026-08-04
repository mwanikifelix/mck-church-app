import { defineStore } from "pinia";
import groupsService from "../services/groups.service";

export const useGroupsStore = defineStore("groups", {
  state: () => ({
    items: [],
    loading: false,
  }),
  actions: {
    async fetchAll() {
      this.loading = true;
      try {
        const { data } = await groupsService.list();
        this.items = data.results || data;
      } finally {
        this.loading = false;
      }
    },
  },
});
