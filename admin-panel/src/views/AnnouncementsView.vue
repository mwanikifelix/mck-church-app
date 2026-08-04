<template>
  <NavBar />
  <div style="padding:2rem; font-family:sans-serif;">
    <h1>Announcements</h1>
    <p v-if="loading">Loading...</p>
    <ul v-else>
      <li v-for="a in announcements" :key="a.id">
        <strong>{{ a.title }}</strong> — {{ a.body }}
        <span v-if="a.is_pinned"> (pinned)</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import NavBar from "../components/NavBar.vue";
import contentService from "../services/content.service";

const announcements = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const { data } = await contentService.listAnnouncements();
    announcements.value = data.results || data;
  } finally {
    loading.value = false;
  }
});
</script>
