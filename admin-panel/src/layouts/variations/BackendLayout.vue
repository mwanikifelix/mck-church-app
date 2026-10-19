<script setup>
import { useTemplateStore } from "@/store/template";

import BaseLayout from "@/layouts/BaseLayout.vue";

// Main store
const store = useTemplateStore();

// Set default elements for this layout
store.setLayout({
  header: true,
  sidebar: true,
  sideOverlay: false,
  footer: true,
});

// Set various template options for this layout variation
store.headerStyle({ mode: "dark" });
store.mainContent({ mode: "full" });
</script>

<template>
  <BaseLayout>
    <RouterView />
  </BaseLayout>
</template>
