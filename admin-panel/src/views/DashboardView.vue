<template>
  <div class="dashboard-grid">
    <Card v-for="stat in stats" :key="stat.label" class="stat-card">
      <template #content>
        <div class="stat-content">
          <i :class="stat.icon" class="stat-icon"></i>
          <div>
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Card from "primevue/card";
import { useAuthStore } from "../store/auth";
import membersService from "../services/members.service";
import churchService from "../services/church.service";

const auth = useAuthStore();
const stats = ref([
  { label: "Welcome", value: auth.user?.full_name || "-", icon: "pi pi-user" },
  { label: "Members", value: "...", icon: "pi pi-users" },
  { label: "Pending Join Requests", value: "...", icon: "pi pi-clock" },
]);

onMounted(async () => {
  try {
    const { data } = await membersService.list();
    stats.value[1].value = (data.results || data).length;
  } catch {
    stats.value[1].value = "-";
  }
  try {
    const { data } = await churchService.listJoinRequests({ status: "pending" });
    stats.value[2].value = (data.results || data).length;
  } catch {
    stats.value[2].value = "-";
  }
});
</script>

<style scoped>
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}
.stat-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.stat-icon {
  font-size: 1.75rem;
  color: #38bdf8;
}
.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
}
.stat-label {
  font-size: 0.85rem;
  color: #64748b;
}
</style>
