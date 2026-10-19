<script setup>
/**
 * Label + control + hint + error wrapper.
 *
 * Replaces the repeated `.form-field` blocks that were duplicated across
 * views with slightly different markup each time.
 */
defineProps({
  label: { type: String, default: "" },
  required: { type: Boolean, default: false },
  hint: { type: String, default: "" },
  // Validation message; when present the control renders as invalid
  error: { type: String, default: "" },
  fieldId: { type: String, default: "" },
});
</script>

<template>
  <div class="mb-3 app-field">
    <label
      v-if="label"
      :for="fieldId || undefined"
      class="form-label d-flex align-items-center gap-1 mb-1"
    >
      {{ label }}
      <span v-if="required" class="text-danger" aria-hidden="true">*</span>
    </label>

    <slot></slot>

    <div v-if="error" class="text-danger fs-sm mt-1 d-flex align-items-center gap-1">
      <i class="fa fa-exclamation-circle"></i>
      <span>{{ error }}</span>
    </div>
    <div v-else-if="hint" class="text-muted fs-sm mt-1">
      {{ hint }}
    </div>
  </div>
</template>
