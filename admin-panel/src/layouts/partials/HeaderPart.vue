<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useTemplateStore } from "@/store/template";
import { useAuthStore } from "@/store/auth";

const route = useRoute();
const router = useRouter();
const store = useTemplateStore();
const auth = useAuthStore();

// Current page title from the route meta
const pageTitle = computed(() => route.meta.title || "Dashboard");

// Available color themes (must match the theme-* classes in styles.scss)
const colorThemes = [
  { id: "wesley", label: "Wesley", swatch: "#0b6bd8" },
  { id: "modern", label: "Modern", swatch: "#0c91cf" },
  { id: "city", label: "City", swatch: "#db3954" },
  { id: "flat", label: "Flat", swatch: "#069fba" },
  { id: "amethyst", label: "Amethyst", swatch: "#6366f1" },
  { id: "smooth", label: "Smooth", swatch: "#d4428b" },
];

// Initials for the avatar chip
const initials = computed(() => {
  const name = auth.user?.full_name || auth.user?.email || "";
  return (
    name
      .split(" ")
      .filter(Boolean)
      .slice(0, 2)
      .map((part) => part[0].toUpperCase())
      .join("") || "?"
  );
});

function handleLogout() {
  auth.logout();
  router.push({ name: "login" });
}
</script>

<template>
  <header id="page-header">
    <slot>
      <!-- Header Content -->
      <div class="content-header">
        <slot name="content">
          <!-- Left Section -->
          <div class="d-flex align-items-center">
            <slot name="content-left">
              <!-- Toggle Sidebar (mobile) -->
              <button
                type="button"
                class="btn btn-sm btn-alt-secondary me-2 d-lg-none"
                aria-label="Toggle navigation"
                @click="store.sidebar({ mode: 'toggle' })"
              >
                <i class="fa fa-fw fa-bars"></i>
              </button>
              <!-- END Toggle Sidebar -->

              <!-- Page Title -->
              <div class="d-flex flex-column">
                <span class="fs-sm fw-semibold text-uppercase opacity-50 lh-1">
                  MCK Wesley
                </span>
                <span class="fw-bold lh-sm d-none d-sm-inline">
                  {{ pageTitle }}
                </span>
              </div>
              <!-- END Page Title -->
            </slot>
          </div>
          <!-- END Left Section -->

          <!-- Right Section -->
          <div class="d-flex align-items-center">
            <slot name="content-right">
              <!-- Color Theme -->
              <div class="dropdown d-inline-block me-1">
                <button
                  type="button"
                  class="btn btn-sm btn-alt-secondary"
                  id="header-color-theme-dropdown"
                  data-bs-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                  aria-label="Change color theme"
                >
                  <i class="fa fa-fw fa-palette"></i>
                </button>
                <div
                  class="dropdown-menu dropdown-menu-end smini-hide border-0"
                  aria-labelledby="header-color-theme-dropdown"
                >
                  <div class="px-3 py-1 fs-sm fw-semibold text-uppercase opacity-50">
                    Color theme
                  </div>
                  <button
                    v-for="theme in colorThemes"
                    :key="theme.id"
                    type="button"
                    class="dropdown-item d-flex align-items-center gap-2"
                    :class="{ active: store.settings.colorTheme === theme.id }"
                    @click="store.setColorTheme({ theme: theme.id })"
                  >
                    <span
                      class="theme-swatch rounded-circle"
                      :style="{ background: theme.swatch }"
                    ></span>
                    <span class="fs-sm fw-medium">{{ theme.label }}</span>
                    <i
                      v-if="store.settings.colorTheme === theme.id"
                      class="fa fa-check ms-auto fs-xs opacity-50"
                    ></i>
                  </button>
                </div>
              </div>
              <!-- END Color Theme -->

              <!-- Dark Mode -->
              <div class="dropdown d-inline-block mx-1">
                <button
                  type="button"
                  class="btn btn-sm btn-alt-secondary"
                  id="header-dark-mode-dropdown"
                  data-bs-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                  aria-label="Toggle dark mode"
                >
                  <i
                    v-if="!store.settings.darkModeActive"
                    class="far fa-fw fa-moon"
                  ></i>
                  <i v-else class="fa fa-fw fa-moon"></i>
                </button>
                <div
                  class="dropdown-menu dropdown-menu-end smini-hide border-0"
                  aria-labelledby="header-dark-mode-dropdown"
                >
                  <button
                    type="button"
                    class="dropdown-item d-flex align-items-center gap-2"
                    :class="{ active: store.settings.darkMode === 'off' }"
                    @click="store.darkMode({ mode: 'off' })"
                  >
                    <i class="far fa-sun fa-fw opacity-50"></i>
                    <span class="fs-sm fw-medium">Light</span>
                  </button>
                  <button
                    type="button"
                    class="dropdown-item d-flex align-items-center gap-2"
                    :class="{ active: store.settings.darkMode === 'on' }"
                    @click="store.darkMode({ mode: 'on' })"
                  >
                    <i class="far fa-moon fa-fw opacity-50"></i>
                    <span class="fs-sm fw-medium">Dark</span>
                  </button>
                  <button
                    type="button"
                    class="dropdown-item d-flex align-items-center gap-2"
                    :class="{ active: store.settings.darkMode === 'system' }"
                    @click="store.darkMode({ mode: 'system' })"
                  >
                    <i class="fa fa-desktop fa-fw opacity-50"></i>
                    <span class="fs-sm fw-medium">System</span>
                  </button>
                </div>
              </div>
              <!-- END Dark Mode -->

              <!-- User Dropdown -->
              <div class="dropdown d-inline-block ms-1">
                <button
                  type="button"
                  class="btn btn-sm btn-alt-secondary d-flex align-items-center gap-2"
                  id="header-user-dropdown"
                  data-bs-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  <span
                    class="d-inline-flex align-items-center justify-content-center bg-primary text-white rounded-circle fw-bold"
                    style="width: 1.75rem; height: 1.75rem; font-size: 0.7rem"
                  >
                    {{ initials }}
                  </span>
                  <span class="d-none d-md-inline fw-medium text-truncate" style="max-width: 8rem">
                    {{ auth.user?.full_name || auth.user?.email }}
                  </span>
                  <i class="fa fa-fw fa-chevron-down fs-xs opacity-50"></i>
                </button>
                <div
                  class="dropdown-menu dropdown-menu-end fs-sm border-0"
                  aria-labelledby="header-user-dropdown"
                >
                  <div class="px-3 py-2 d-none d-md-block">
                    <div class="fw-semibold">
                      {{ auth.user?.full_name }}
                    </div>
                    <div class="text-muted text-truncate" style="max-width: 14rem">
                      {{ auth.user?.email }}
                    </div>
                  </div>
                  <div class="dropdown-divider"></div>
                  <button
                    type="button"
                    class="dropdown-item d-flex align-items-center gap-2"
                    @click="handleLogout"
                  >
                    <i class="fa fa-sign-out-alt fa-fw opacity-50"></i>
                    <span>Sign out</span>
                  </button>
                </div>
              </div>
              <!-- END User Dropdown -->
            </slot>
          </div>
          <!-- END Right Section -->
        </slot>
      </div>
      <!-- END Header Content -->
    </slot>
  </header>
</template>
