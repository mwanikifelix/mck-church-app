<template>
  <div>
    <!-- Header -->
    <div class="header-row mb-3">
      <div>
        <h2 class="section-title mb-0">Giving Review</h2>
        <p class="text-muted fs-sm mb-0">
          {{ donations.length }} {{ donations.length === 1 ? "donation" : "donations" }}
        </p>
      </div>
    </div>

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
</template>

<script setup>
import { ref, onMounted } from "vue";
import givingService from "../services/giving.service";

const donations = ref([]);
const loading = ref(true);

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
  } finally {
    loading.value = false;
  }
});
</script>
