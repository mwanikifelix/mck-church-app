<template>
  <NavBar />
  <div style="padding:2rem; font-family:sans-serif;">
    <h1>Growth-Track Groups</h1>
    <p v-if="store.loading">Loading...</p>
    <table v-else border="1" cellpadding="8" style="width:100%; border-collapse:collapse;">
      <thead>
        <tr><th>Name</th><th>Branch</th><th>Age Range</th><th>Active</th></tr>
      </thead>
      <tbody>
        <tr v-for="g in store.items" :key="g.id">
          <td>{{ g.name }}</td>
          <td>{{ g.branch }}</td>
          <td>{{ g.min_age }} - {{ g.max_age }}</td>
          <td>{{ g.is_active ? "Yes" : "No" }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import NavBar from "../components/NavBar.vue";
import { useGroupsStore } from "../store/groups";

const store = useGroupsStore();
onMounted(() => store.fetchAll());
</script>
