<template>
  <NavBar />
  <div style="padding:2rem; font-family:sans-serif;">
    <h1>Events</h1>
    <p v-if="loading">Loading...</p>
    <table v-else border="1" cellpadding="8" style="width:100%; border-collapse:collapse;">
      <thead>
        <tr><th>Title</th><th>Start</th><th>Location</th><th>RSVPs</th></tr>
      </thead>
      <tbody>
        <tr v-for="e in events" :key="e.id">
          <td>{{ e.title }}</td>
          <td>{{ new Date(e.start_time).toLocaleString() }}</td>
          <td>{{ e.location }}</td>
          <td>{{ e.rsvp_count }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import NavBar from "../components/NavBar.vue";
import eventsService from "../services/events.service";

const events = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const { data } = await eventsService.list();
    events.value = data.results || data;
  } finally {
    loading.value = false;
  }
});
</script>
