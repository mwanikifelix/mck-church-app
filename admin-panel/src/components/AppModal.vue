<script setup>
import { watch, onBeforeUnmount, ref } from "vue";

/**
 * Bootstrap-styled modal that mirrors PrimeVue's Dialog API closely enough
 * to make migration mechanical:
 *
 *   <AppModal v-model:visible="show" title="New Member" size="sm">
 *     ...body...
 *     <template #footer> ... </template>
 *   </AppModal>
 *
 * Unlike the old inline `style="width:460px"` dialogs, width is fluid:
 * it fills the viewport on phones and caps at `size` on larger screens.
 */
const props = defineProps({
  visible: { type: Boolean, default: false },
  title: { type: String, default: "" },
  // 'sm' | '' | 'lg' | 'xl'
  size: { type: String, default: "sm" },
  // Hides the header close button (e.g. destructive confirmations)
  closable: { type: Boolean, default: true },
  // Prevents dismissing by clicking the backdrop / pressing Escape
  static: { type: Boolean, default: false },
  // Subtitle rendered under the title
  subtitle: { type: String, default: "" },
});

const emit = defineEmits(["update:visible", "show", "hide"]);

const root = ref(null);

function close() {
  if (props.static) return;
  emit("update:visible", false);
}

function onKeydown(e) {
  if (e.key === "Escape" && props.visible) close();
}

// Lock body scroll while open, listen for Escape
watch(
  () => props.visible,
  (open) => {
    document.body.style.overflow = open ? "hidden" : "";
    if (open) emit("show");
    else emit("hide");
  }
);

onBeforeUnmount(() => {
  document.body.style.overflow = "";
});

if (typeof window !== "undefined") {
  window.addEventListener("keydown", onKeydown);
}
</script>

<template>
  <teleport to="body">
    <transition name="modal-fade">
      <div
        v-if="visible"
        ref="root"
        class="modal d-block"
        tabindex="-1"
        role="dialog"
        :aria-modal="true"
        :aria-label="title || undefined"
      >
        <!-- Backdrop -->
        <div class="modal-backdrop fade show" @click="close"></div>

        <div class="modal-dialog" :class="size ? `modal-${size}` : null">
          <div class="modal-content">
            <!-- Header -->
            <div v-if="title || closable" class="modal-header">
              <div>
                <h5 class="modal-title fw-bold mb-0">{{ title }}</h5>
                <div v-if="subtitle" class="fs-sm text-muted mt-1">
                  {{ subtitle }}
                </div>
              </div>
              <button
                v-if="closable"
                type="button"
                class="btn-close"
                aria-label="Close"
                @click="close"
              ></button>
            </div>

            <!-- Body -->
            <div class="modal-body">
              <slot></slot>
            </div>

            <!-- Footer -->
            <div v-if="$slots.footer" class="modal-footer">
              <slot name="footer"></slot>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/*
 * Bootstrap ships .modal-backdrop as a sibling of .modal with z-index 1040.
 * We nest it inside .modal, so it must be pushed behind .modal-dialog or it
 * would paint over the dialog and swallow all pointer events.
 */
.modal .modal-backdrop {
  z-index: 0;
}
.modal .modal-dialog {
  position: relative;
  z-index: 1;
}

/* Keep dialogs inside the viewport on small screens */
@media (max-width: 575.98px) {
  .modal-dialog {
    max-width: calc(100% - 1rem);
    margin: 0.5rem auto;
  }
  .modal-body {
    max-height: calc(100vh - 12rem);
    overflow-y: auto;
  }
}
</style>
