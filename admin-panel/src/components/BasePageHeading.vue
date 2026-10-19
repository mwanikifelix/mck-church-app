<script setup>
// Branded page heading — a Wesley-colored gradient band that opens every
// admin page, with an icon chip, title, subtitle and an action slot.
//
//   <BasePageHeading
//     title="Members"
//     :subtitle="`${members.length} registered`"
//     icon="fa-users"
//   >
//     <template #extra>
//       <button class="btn btn-light">New Member</button>
//     </template>
//   </BasePageHeading>
defineProps({
  title: {
    type: String,
    description: "The title of the page heading",
  },
  subtitle: {
    type: String,
    description: "The subtitle / count line of the page heading",
  },
  icon: {
    type: String,
    description: "FontAwesome icon classes for the heading chip",
  },
  tone: {
    type: String,
    default: "primary",
    description: "Heading color tone: primary | green | dark",
  },
});
</script>

<template>
  <div class="page-heading" :class="`page-heading-${tone}`">
    <div class="content content-full">
      <div
        class="d-flex flex-column flex-sm-row justify-content-sm-between align-items-sm-center gap-3 py-2"
      >
        <div class="d-flex align-items-center gap-3 min-w-0">
          <span v-if="icon" class="page-heading-icon">
            <i class="fa fa-fw" :class="icon"></i>
          </span>
          <div class="min-w-0">
            <h1 v-if="title" class="h3 fw-bold mb-1 text-white text-truncate">
              {{ title }}
            </h1>
            <p v-if="subtitle" class="fs-sm mb-0 opacity-75 text-white">
              {{ subtitle }}
            </p>
          </div>
        </div>
        <div v-if="$slots.extra" class="flex-shrink-0">
          <slot name="extra"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.min-w-0 {
  min-width: 0;
}
</style>
