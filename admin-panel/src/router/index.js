import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../store/auth";

const routes = [
  { path: "/login", name: "login", component: () => import("../views/LoginView.vue"), meta: { title: "Sign In" } },
  {
    path: "/",
    component: () => import("../layouts/BaseLayout.vue"),
    meta: { requiresAuth: true },
    children: [
      { path: "", name: "dashboard", component: () => import("../views/DashboardView.vue"), meta: { title: "Dashboard" } },
      { path: "members", name: "members", component: () => import("../views/MembersView.vue"), meta: { title: "Members" } },
      { path: "branches", name: "branches", component: () => import("../views/BranchesView.vue"), meta: { title: "Branches" } },
      { path: "content-library", name: "content-library", component: () => import("../views/ContentLibraryView.vue"), meta: { title: "Content Library" } },
      { path: "about-content", name: "about-content", component: () => import("../views/AboutContentView.vue"), meta: { title: "About Page Content" } },
      { path: "registration-windows", name: "registration-windows", component: () => import("../views/RegistrationWindowsView.vue"), meta: { title: "Registration Windows" } },
      { path: "hbc", name: "hbc", component: () => import("../views/HBCView.vue"), meta: { title: "HBC Groups" } },
      { path: "departments", name: "departments", component: () => import("../views/DepartmentsView.vue"), meta: { title: "Departments" } },
      { path: "groups", name: "groups", component: () => import("../views/GroupsView.vue"), meta: { title: "Growth-Track Groups" } },
      { path: "events", name: "events", component: () => import("../views/EventsView.vue"), meta: { title: "Events" } },
      { path: "announcements", name: "announcements", component: () => import("../views/AnnouncementsView.vue"), meta: { title: "Announcements" } },
      { path: "giving", name: "giving", component: () => import("../views/GivingReviewView.vue"), meta: { title: "Giving" } },
      { path: "pastoral-care", name: "pastoral-care", component: () => import("../views/PastoralCareView.vue"), meta: { title: "Pastoral Care" } },
      { path: "roles", name: "roles", component: () => import("../views/RolesPermissionsView.vue"), meta: { title: "Roles & Permissions" } },
    ],
  },
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

router.afterEach((to) => {
  const title = to.meta.title;
  document.title = title ? `${title} — MCK Wesley Church` : "MCK Wesley Church — Admin";
});

export default router;
