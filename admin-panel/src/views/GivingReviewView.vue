<template>
  <NavBar />
  <div style="padding:2rem; font-family:sans-serif;">
    <h1>Giving Review</h1>
    <p v-if="loading">Loading...</p>
    <table v-else border="1" cellpadding="8" style="width:100%; border-collapse:collapse;">
      <thead>
        <tr><th>Member</th><th>Account</th><th>Amount</th><th>Date</th></tr>
      </thead>
      <tbody>
        <tr v-for="d in donations" :key="d.id">
          <td>{{ d.member_name }}</td>
          <td>{{ d.account_code_display }}</td>
          <td>{{ d.amount }}</td>
          <td>{{ new Date(d.created_at).toLocaleDateString() }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import NavBar from "../components/NavBar.vue";
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
