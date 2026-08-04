<template>
  <nav style="display:flex; gap:1rem; padding:1rem; background:#222; color:#fff;">
    <strong style="margin-right:2rem;">MCK Admin</strong>
    <router-link to="/" style="color:#fff;">Dashboard</router-link>
    <router-link to="/groups" style="color:#fff;">Groups</router-link>
    <router-link to="/events" style="color:#fff;">Events</router-link>
    <router-link to="/announcements" style="color:#fff;">Announcements</router-link>
    <router-link to="/giving" style="color:#fff;">Giving</router-link>
    <router-link to="/roles" style="color:#fff;">Roles</router-link>
    <span style="margin-left:auto;">{{ auth.user?.full_name }}</span>
    <button @click="handleLogout">Logout</button>
  </nav>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useAuthStore } from "../store/auth";

const auth = useAuthStore();
const router = useRouter();

function handleLogout() {
  auth.logout();
  router.push({ name: "login" });
}
</script>
