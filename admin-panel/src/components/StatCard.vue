<script setup>
/**
 * Dashboard KPI card. Colour comes from `tone` so a row of these reads as a
 * palette rather than four identical white boxes.
 */
defineProps({
  label: { type: String, default: "" },
  value: { type: [String, Number], default: "—" },
  icon: { type: String, default: "fa-chart-line" },
  tone: {
    type: String,
    default: "primary", // primary | success | warning | danger | info | secondary
  },
  hint: { type: String, default: ""},
  loading: { type: Boolean, default: false },
});
</script>

<template>
  <div class="block rounded-3 h-100" :class="`block-themed bg-${tone}-subtle`">
    <div class="block-content p-3">
      <div class="d-flex align-items-center justify-content-between gap-3">
        <div class="min-w-0">
          <div class="fs-xs text-uppercase fw-semibold text-muted text-truncate">
            {{ label }}
          </div>
          <div class="fs-2 fw-bold lh-sm mt-1 text-truncate">
            <span v-if="loading" class="placeholder-glow">
              <span class="placeholder rounded" style="width: 3rem; height: 1.6rem"></span>
            </span>
            <template v-else>{{ value }}</template>
          </div>
          <div v-if="hint" class="fs-sm text-muted text-truncate mt-1">
            {{ hint }}
          </div>
        </div>

        <span
          class="d-inline-flex align-items-center justify-content-center rounded-3 flex-shrink-0"
          :class="`bg-${tone} text-white`"
          style="width: 2.75rem; height: 2.75rem"
        >
          <i class="fa fa-lg" :class="icon"></i>
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.min-w-0 {
  min-width: 0;
}
</style>
