<script setup>
import { onMounted } from "vue";

import BaseNavigation from "@/components/BaseNavigation.vue";

// SimpleBar custom scrolling
import SimpleBar from "simplebar";

// Sidebar navigation structure
import menu from "@/data/menu";

const navigation = menu.main;

// Component properties
defineProps({
  withMiniNav: {
    type: Boolean,
    default: false,
    description: "If the sidebar is in Mini Nav Mode",
  },
});

// Init SimpleBar (custom scrolling)
onMounted(() => {
  new SimpleBar(document.getElementById("simplebar-sidebar"));
});
</script>

<template>
  <nav
    id="sidebar"
    :class="{ 'with-mini-nav': withMiniNav }"
    aria-label="Main Navigation"
  >
    <slot>
      <!-- Side Header -->
      <div class="content-header">
        <slot name="header">
          <!-- Brand -->
          <RouterLink
            :to="{ name: 'dashboard' }"
            class="fw-semibold text-dual d-flex align-items-center gap-2 text-decoration-none"
          >
            <span class="smini-visible">
              <i class="fa fa-church text-primary"></i>
            </span>
            <span class="smini-hide fs-5 tracking-wider">
              MCK Wesley
              <span class="fw-normal">Admin</span>
            </span>
          </RouterLink>
          <!-- END Brand -->
        </slot>
      </div>
      <!-- END Side Header -->

      <!-- Sidebar Scrolling -->
      <div id="simplebar-sidebar" class="js-sidebar-scroll">
        <slot name="content">
          <!-- Side Navigation -->
          <div class="content-side">
            <BaseNavigation :nodes="navigation" />
          </div>
          <!-- END Side Navigation -->
        </slot>
      </div>
      <!-- END Sidebar Scrolling -->
    </slot>
  </nav>
</template>
