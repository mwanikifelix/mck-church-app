import { reactive } from "vue";

/**
 * Lightweight toast store that mirrors the PrimeVue `useToast().add()` API.
 *
 * Views were written against PrimeVue's signature:
 *   toast.add({ severity, summary, detail, life })
 * Keeping that shape means none of the existing error handling has to change
 * while the UI layer moves over to Bootstrap/OneUI.
 */

export const toastState = reactive({ items: [] });

let uid = 0;

const DEFAULT_LIFE = 3000;

export function useToast() {
  function add(payload = {}) {
    const item = {
      id: ++uid,
      severity: payload.severity || "info",
      summary: payload.summary || "",
      detail: payload.detail || "",
      life: typeof payload.life === "number" ? payload.life : DEFAULT_LIFE,
      group: payload.group,
      closable: payload.closable !== false,
      visible: true,
    };

    toastState.items.push(item);

    if (item.life > 0) {
      setTimeout(() => dismiss(item.id), item.life);
    }

    return item;
  }

  function dismiss(id) {
    const idx = toastState.items.findIndex((t) => t.id === id);
    if (idx !== -1) toastState.items.splice(idx, 1);
  }

  function clear() {
    toastState.items.splice(0, toastState.items.length);
  }

  return { add, dismiss, clear };
}
