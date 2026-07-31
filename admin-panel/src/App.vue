<template>
  <div style="font-family: sans-serif; padding: 2rem;">
    <h1>MCK Church App — Admin Panel</h1>
    <p>Placeholder screen. Backend API: {{ apiBase }}</p>
  </div>
</template>

<script setup>
const apiBase = import.meta.env.VITE_API_BASE_URL;
</script>
