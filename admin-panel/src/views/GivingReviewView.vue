<template>
  <div>
    <BasePageHeading
      title="Giving Review"
      icon="fa-hand-holding-heart"
      tone="green"
      :subtitle="scopeLabel"
    />

    <div class="content">
    <AppDataTable
      :rows="donations"
      :columns="columns"
      :loading="loading"
      :page-size="15"
      search-placeholder="Search member or account…"
      export-name="giving-review"
      empty-text="No donations recorded yet."
      empty-icon="fa-hand-holding-heart"
    >
      <template #date="{ value }">
        <span v-if="value">{{ new Date(value).toLocaleDateString() }}</span>
        <span v-else class="text-muted">—</span>
      </template>
    </AppDataTable>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useToast } from "../composables/useToast";
import { useAuthStore } from "../store/auth";
import givingService from "../services/giving.service";

const toast = useToast();
const auth = useAuthStore();

const donations = ref([]);
const loading = ref(true);

// The API only returns church-wide donations to finance roles; everyone
// else gets their own, so say which list is on screen.
const scopeLabel = computed(() => {
  const count = `${donations.value.length} ${
    donations.value.length === 1 ? "donation" : "donations"
  }`;
  return auth.hasPermission("finance.view") ? count : `${count} (your own only)`;
});

const columns = [
  { field: "member_name", header: "Member", sortable: true, strong: true },
  { field: "account_code_display", header: "Account", sortable: true },
  { field: "amount", header: "Amount", sortable: true },
  { field: "created_at", header: "Date", sortable: true, slot: "date" },
];

onMounted(async () => {
  try {
    const { data } = await givingService.listDonations();
    donations.value = data.results || data;
  } catch {
    donations.value = [];
    toast.add({
      severity: "error",
      summary: "Could not load donations",
      detail: "Check that the API is running.",
      life: 5000,
    });
  } finally {
    loading.value = false;
  }
});
</script>
