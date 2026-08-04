<template>
  <NavBar />
  <div style="padding:2rem; font-family:sans-serif;">
    <h1>Welcome, {{ auth.user?.full_name }}</h1>
    <p>Membership No: {{ auth.user?.membership_number }}</p>
  </div>
</template>

<script setup>
import NavBar from "../components/NavBar.vue";
import { useAuthStore } from "../store/auth";

const auth = useAuthStore();
</script>
