<template>
  <div>
    <!-- KPI row -->
    <div class="row g-3 mb-4">
      <div v-for="stat in stats" :key="stat.label" class="col-12 col-sm-6 col-xl-3">
        <StatCard
          :label="stat.label"
          :value="stat.value"
          :icon="stat.icon"
          :tone="stat.tone"
          :hint="stat.hint"
          :loading="loading"
        />
      </div>
    </div>

    <!-- Secondary panels -->
    <div class="row g-3">
      <div class="col-12 col-lg-6">
        <BaseBlock title="Welcome" subtitle="Signed in to the administration panel">
          <div class="d-flex align-items-center gap-3">
            <span
              class="d-inline-flex align-items-center justify-content-center rounded-circle bg-primary text-white fw-bold"
              style="width: 3rem; height: 3rem"
            >
              {{ initials }}
            </span>
            <div class="min-w-0">
              <div class="fw-bold text-truncate">{{ auth.user?.full_name || "—" }}</div>
              <div class="fs-sm text-muted text-truncate">
                {{ auth.user?.email }}
              </div>
              <div class="mt-1">
                <span
                  class="badge rounded-pill"
                  :class="auth.user?.is_superuser ? 'bg-primary' : 'bg-secondary'"
                >
                  {{ auth.user?.role?.name || (auth.user?.is_superuser ? "Superuser" : "Member") }}
                </span>
              </div>
            </div>
          </div>
        </BaseBlock>
      </div>

      <div class="col-12 col-lg-6">
        <BaseBlock title="Quick actions" subtitle="Common administrative tasks">
          <div class="d-flex flex-wrap gap-2">
            <router-link :to="{ name: 'members' }" class="btn btn-sm btn-alt-primary">
              <i class="fa fa-users me-1"></i> Manage members
            </router-link>
            <router-link :to="{ name: 'events' }" class="btn btn-sm btn-alt-secondary">
              <i class="fa fa-calendar-alt me-1"></i> Events
            </router-link>
            <router-link :to="{ name: 'announcements' }" class="btn btn-sm btn-alt-secondary">
              <i class="fa fa-bullhorn me-1"></i> Announcements
            </router-link>
            <router-link :to="{ name: 'roles' }" class="btn btn-sm btn-alt-secondary">
              <i class="fa fa-user-shield me-1"></i> Permissions
            </router-link>
          </div>
        </BaseBlock>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useAuthStore } from "../store/auth";
import membersService from "../services/members.service";
import churchService from "../services/church.service";

const auth = useAuthStore();
const loading = ref(true);

const stats = ref([
  { label: "Members", value: "—", icon: "fa fa-users", tone: "primary", hint: "Total registered" },
  { label: "Pending Join Requests", value: "—", icon: "fa fa-user-clock", tone: "warning", hint: "Awaiting review" },
  { label: "Branches", value: "—", icon: "fa fa-map-marker-alt", tone: "success", hint: "Church locations" },
  { label: "Events", value: "—", icon: "fa fa-calendar-check", tone: "info", hint: "Scheduled" },
]);

const initials = computed(() =>
  (auth.user?.full_name || "")
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((p) => p[0].toUpperCase())
    .join("") || "?"
);

async function loadStat(index, fetcher) {
  try {
    const { data } = await fetcher();
    stats.value[index].value = (data.results || data).length;
  } catch {
    stats.value[index].value = "—";
  }
}

onMounted(async () => {
  await Promise.all([
    loadStat(0, () => membersService.list()),
    loadStat(1, () => churchService.listJoinRequests({ status: "pending" })),
  ]);
  loading.value = false;
});
</script>

<style scoped>
.min-w-0 {
  min-width: 0;
}
</style>
