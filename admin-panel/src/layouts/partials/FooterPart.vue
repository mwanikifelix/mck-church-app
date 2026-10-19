<script setup>
import { useTemplateStore } from "@/store/template";

// Main store
const store = useTemplateStore();
</script>

<template>
  <!-- Footer -->
  <footer id="page-footer">
    <slot>
      <div class="bg-body-light">
        <div class="content py-3">
          <div class="row fs-sm">
            <div class="col-sm-6 order-sm-2 py-1 text-center text-sm-end">
              <slot name="content-right">
                MCK Wesley Church
                <span class="opacity-50">&middot;</span>
                Administration Panel
              </slot>
            </div>
            <div class="col-sm-6 order-sm-1 py-1 text-center text-sm-start">
              <slot name="content-left">
                <span class="fw-semibold">{{ store.app.name }}</span>
                &nbsp;v{{ store.app.version }}
                &nbsp;&copy; {{ store.app.copyright }}
              </slot>
            </div>
          </div>
        </div>
      </div>
    </slot>
  </footer>
  <!-- END Footer -->
</template>
