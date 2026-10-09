<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="sidebar-brand">MCK WESLEY Admin</div>
      <nav class="sidebar-nav">
        <router-link v-for="item in navItems" :key="item.to" :to="item.to" class="nav-item">
          <i :class="item.icon"></i>
          <span>{{ item.label }}</span>
        </router-link>
      </nav>
    </aside>

    <div class="main-column">
      <header class="topbar">
        <span class="topbar-title">{{ route.meta.title || "" }}</span>
        <div class="topbar-user">
          <span>{{ auth.user?.full_name }}</span>
          <Button icon="pi pi-sign-out" severity="secondary" text @click="handleLogout" />
        </div>
      </header>
      <main class="content">
        <router-view />
      </main>
    </div>

    <Toast />
    <ConfirmDialog />
  </div>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "../store/auth";
import Button from "primevue/button";
import Toast from "primevue/toast";
import ConfirmDialog from "primevue/confirmdialog";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();

const navItems = [
  { to: "/", label: "Dashboard", icon: "pi pi-home" },
  { to: "/members", label: "Members", icon: "pi pi-users" },
  { to: "/branches", label: "Branches", icon: "pi pi-map-marker" },
  { to: "/content-library", label: "Content Library", icon: "pi pi-book" },
  { to: "/about-content", label: "About Page Content", icon: "pi pi-info-circle" },
  { to: "/registration-windows", label: "Registration Windows", icon: "pi pi-calendar-times" },
  { to: "/hbc", label: "HBC Groups", icon: "pi pi-sitemap" },
  { to: "/departments", label: "Departments", icon: "pi pi-building" },
  { to: "/groups", label: "Growth-Track Groups", icon: "pi pi-share-alt" },
  { to: "/events", label: "Events", icon: "pi pi-calendar" },
  { to: "/announcements", label: "Announcements", icon: "pi pi-megaphone" },
  { to: "/giving", label: "Giving", icon: "pi pi-wallet" },
  { to: "/pastoral-care", label: "Pastoral Care", icon: "pi pi-heart" },
  { to: "/roles", label: "Roles & Permissions", icon: "pi pi-shield" },
];

function handleLogout() {
  auth.logout();
  router.push({ name: "login" });
}
</script>

<style scoped>
.app-shell {
  display: flex;
  min-height: 100vh;
  background: #f4f6f9;
}
.sidebar {
  width: 240px;
  background: #1e293b;
  color: #fff;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}
.sidebar-brand {
  padding: 1.25rem 1.5rem;
  font-weight: 700;
  font-size: 1.1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.sidebar-nav {
  display: flex;
  flex-direction: column;
  padding: 0.75rem 0;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.7rem 1.5rem;
  color: #cbd5e1;
  text-decoration: none;
  font-size: 0.9rem;
}
.nav-item:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #fff;
}
.nav-item.router-link-active {
  background: #334155;
  color: #fff;
  border-left: 3px solid #38bdf8;
}
.main-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.topbar {
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  flex-shrink: 0;
}
.topbar-title {
  font-weight: 600;
  color: #1e293b;
}
.topbar-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #475569;
}
.content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
}
</style>
