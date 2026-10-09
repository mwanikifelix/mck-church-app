<template>
  <DataTable :value="donations" :loading="loading" paginator :rows="15" sortMode="multiple">
    <Column field="member_name" header="Member" sortable />
    <Column field="account_code_display" header="Account" sortable />
    <Column field="amount" header="Amount" sortable />
    <Column header="Date" sortable sortField="created_at">
      <template #body="{ data }">{{ new Date(data.created_at).toLocaleDateString() }}</template>
    </Column>
  </DataTable>
</template>

<script setup>
import { ref, onMounted } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import givingService from "../services/giving.service";

const donations = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const { data } = await givingService.listDonations();
    donations.value = data.results || data;
  } finally {
    loading.value = false;
  }
});
</script>
