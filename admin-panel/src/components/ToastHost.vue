<script setup>
import { toastState } from "@/composables/useToast";

const SEVERITY_MAP = {
  success: { alert: "alert-success", icon: "fa-check-circle" },
  info: { alert: "alert-info", icon: "fa-info-circle" },
  warn: { alert: "alert-warning", icon: "fa-exclamation-triangle" },
  warning: { alert: "alert-warning", icon: "fa-exclamation-triangle" },
  error: { alert: "alert-danger", icon: "fa-times-circle" },
  danger: { alert: "alert-danger", icon: "fa-times-circle" },
  secondary: { alert: "alert-secondary", icon: "fa-bell" },
};

function styleFor(severity) {
  return SEVERITY_MAP[severity] || SEVERITY_MAP.info;
}
</script>

<template>
  <!-- Accessible live region so screen readers announce new toasts -->
  <div
    class="toast-container position-fixed top-0 end-0 p-3"
    style="z-index: 1090"
    aria-live="polite"
    aria-atomic="true"
  >
    <transition-group name="toast-slide">
      <div
        v-for="item in toastState.items"
        :key="item.id"
        class="alert d-flex align-items-start gap-2 mb-2 shadow-lg py-2 px-3"
        :class="styleFor(item.severity).alert"
        role="alert"
      >
        <i
          class="fa mt-1"
          :class="styleFor(item.severity).icon"
          aria-hidden="true"
        ></i>
        <div class="flex-grow-1">
          <div v-if="item.summary" class="fw-bold lh-sm">
            {{ item.summary }}
          </div>
          <div v-if="item.detail" class="fs-sm opacity-90 mt-1">
            {{ item.detail }}
          </div>
        </div>
        <button
          v-if="item.closable"
          type="button"
          class="btn-close btn-close-sm mt-1"
          aria-label="Close"
          @click="toastState.items.splice(toastState.items.indexOf(item), 1)"
        ></button>
      </div>
    </transition-group>
  </div>
</template>

<style scoped>
.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.25s ease;
}
.toast-slide-enter-from,
.toast-slide-leave-to {
  opacity: 0;
  transform: translateX(1.5rem);
}
</style>
