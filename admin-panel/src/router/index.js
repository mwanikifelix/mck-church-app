import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../store/auth";

const routes = [
  { path: "/login", name: "login", component: () => import("../views/LoginView.vue") },
  { path: "/", name: "dashboard", component: () => import("../views/DashboardView.vue"), meta: { requiresAuth: true } },
  { path: "/groups", name: "groups", component: () => import("../views/GroupsView.vue"), meta: { requiresAuth: true } },
  { path: "/events", name: "events", component: () => import("../views/EventsView.vue"), meta: { requiresAuth: true } },
  { path: "/announcements", name: "announcements", component: () => import("../views/AnnouncementsView.vue"), meta: { requiresAuth: true } },
  { path: "/giving", name: "giving", component: () => import("../views/GivingReviewView.vue"), meta: { requiresAuth: true } },
  { path: "/roles", name: "roles", component: () => import("../views/RolesPermissionsView.vue"), meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const auth = useAuthStore();
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: "login" };
  }
});

export default router;
