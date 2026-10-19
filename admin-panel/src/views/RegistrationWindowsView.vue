<template>
  <div>
    <!-- Header -->
    <div class="header-row mb-3">
      <div>
        <h2 class="section-title mb-0">Registration Windows</h2>
        <p class="text-muted fs-sm mb-0">
          {{ windows.length }} {{ windows.length === 1 ? "window" : "windows" }}
        </p>
      </div>
      <button type="button" class="btn btn-primary btn-sm" @click="openCreate">
        <i class="fa fa-plus me-1"></i> New Window
      </button>
    </div>

    <AppDataTable
      :rows="windows"
      :columns="windowColumns"
      :loading="loadingWindows"
      :page-size="10"
      search-placeholder="Search windows…"
      export-name="registration-windows"
      empty-text="No registration windows yet."
      empty-icon="fa-calendar-alt"
    >
      <template #opens="{ value }">
        <span v-if="value">{{ new Date(value).toLocaleString() }}</span>
        <span v-else class="text-muted">—</span>
      </template>

      <template #closes="{ value }">
        <span v-if="value">{{ new Date(value).toLocaleString() }}</span>
        <span v-else class="text-muted">—</span>
      </template>

      <template #status="{ row }">
        <span class="badge rounded-pill" :class="windowStatusClass(row.is_open)">
          <i class="fa fa-circle me-1" style="font-size: 0.5rem; vertical-align: middle"></i>
          {{ row.is_open ? "Open" : "Closed" }}
        </span>
      </template>

      <!--
        `#actions` doubles as AppDataTable's toolbar slot, so the content must
        stay guarded on `row` — the toolbar invokes it without row props.
      -->
      <template #actions="{ row }">
        <div v-if="row" class="d-flex gap-2 justify-content-end">
          <button
            type="button"
            class="btn btn-alt-secondary btn-sm"
            @click="viewRegistrations(row)"
          >
            <i class="fa fa-list me-1"></i> View Registrations
          </button>
        </div>
      </template>
    </AppDataTable>

    <!-- Registrations for the selected window -->
    <template v-if="activeWindow">
      <div class="header-row mb-3 mt-4">
        <div>
          <h2 class="section-title mb-0">
            Registrations — {{ activeWindow.name }}
          </h2>
          <p class="text-muted fs-sm mb-0">
            {{ registrations.length }} recorded
          </p>
        </div>
        <button
          type="button"
          class="btn btn-alt-secondary btn-sm"
          @click="viewRegistrations(activeWindow)"
        >
          <i class="fa fa-sync-alt me-1"></i> Refresh
        </button>
      </div>

      <AppDataTable
        :rows="registrations"
        :columns="registrationColumns"
        :loading="loadingRegistrations"
        :page-size="15"
        search-placeholder="Search member, status or notes…"
        export-name="registrations"
        empty-text="No registrations for this window yet."
        empty-icon="fa-clipboard-list"
      >
        <template #regStatus="{ value }">
          <span class="badge rounded-pill" :class="registrationStatusClass(value)">
            <i class="fa fa-circle me-1" style="font-size: 0.5rem; vertical-align: middle"></i>
            {{ value }}
          </span>
        </template>

        <template #submitted="{ value }">
          <span v-if="value">{{ new Date(value).toLocaleString() }}</span>
          <span v-else class="text-muted">—</span>
        </template>
      </AppDataTable>
    </template>

    <!-- Create dialog -->
    <AppModal
      v-model:visible="showCreate"
      title="New Registration Window"
      subtitle="Open a period during which members can register"
      size="sm"
    >
      <FormField label="Name" required :error="errors.name" field-id="rw-name">
        <input
          id="rw-name"
          v-model="form.name"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errors.name }"
          placeholder="e.g. Catechism 2026 Term 1"
        />
      </FormField>

      <FormField label="Description" :error="errors.description" field-id="rw-desc">
        <textarea
          id="rw-desc"
          v-model="form.description"
          rows="2"
          class="form-control"
          :class="{ 'is-invalid': errors.description }"
          placeholder="Who is this window for?"
        ></textarea>
      </FormField>

      <div class="row g-3">
        <div class="col-12 col-sm-6">
          <FormField label="Opens" required :error="errors.opens_at" field-id="rw-opens">
            <input
              id="rw-opens"
              v-model="form.opens_at"
              type="datetime-local"
              class="form-control"
              :class="{ 'is-invalid': errors.opens_at }"
            />
          </FormField>
        </div>
        <div class="col-12 col-sm-6">
          <FormField label="Closes" required :error="errors.closes_at" field-id="rw-closes">
            <input
              id="rw-closes"
              v-model="form.closes_at"
              type="datetime-local"
              class="form-control"
              :class="{ 'is-invalid': errors.closes_at }"
            />
          </FormField>
        </div>
      </div>

      <template #footer>
        <button type="button" class="btn btn-alt-secondary btn-sm" @click="showCreate = false">
          Cancel
        </button>
        <button
          type="button"
          class="btn btn-primary btn-sm"
          :disabled="creating"
          @click="submitCreate"
        >
          <span v-if="creating" class="spinner-border spinner-border-sm me-1"></span>
          Create window
        </button>
      </template>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "../composables/useToast";
import registrationService from "../services/registration.service";

const toast = useToast();

const windows = ref([]);
const loadingWindows = ref(true);
const registrations = ref([]);
const loadingRegistrations = ref(false);
const activeWindow = ref(null);
const showCreate = ref(false);
const creating = ref(false);

const windowColumns = [
  { field: "name", header: "Name", sortable: true, strong: true },
  { field: "opens_at", header: "Opens", slot: "opens" },
  { field: "closes_at", header: "Closes", slot: "closes" },
  { field: "is_open", header: "Status", slot: "status" },
  { header: "Actions", slot: "actions", align: "end", sortable: false },
];

const registrationColumns = [
  { field: "user_name", header: "Member", sortable: true, strong: true },
  { field: "status", header: "Status", slot: "regStatus" },
  { field: "submitted_at", header: "Submitted", slot: "submitted" },
  { field: "notes", header: "Notes" },
];

const blank = () => ({ name: "", description: "", opens_at: "", closes_at: "" });

const form = ref(blank());
const errors = ref({});

function openCreate() {
  form.value = blank();
  errors.value = {};
  showCreate.value = true;
}

function windowStatusClass(isOpen) {
  return isOpen
    ? "bg-success-subtle text-success-emphasis"
    : "bg-secondary-subtle text-secondary-emphasis";
}

function registrationStatusClass(status) {
  if (status === "completed") return "bg-success-subtle text-success-emphasis";
  if (status === "confirmed") return "bg-info-subtle text-info-emphasis";
  if (status === "pending") return "bg-warning-subtle text-warning-emphasis";
  return "bg-secondary-subtle text-secondary-emphasis";
}

function validate() {
  const e = {};
  if (!form.value.name.trim()) e.name = "Window name is required.";
  if (!form.value.opens_at) e.opens_at = "Opening date and time are required.";
  if (!form.value.closes_at) e.closes_at = "Closing date and time are required.";
  if (
    form.value.opens_at &&
    form.value.closes_at &&
    new Date(form.value.closes_at) <= new Date(form.value.opens_at)
  ) {
    e.closes_at = "Closing time must be after opening time.";
  }

  errors.value = e;
  return Object.keys(e).length === 0;
}

/** Turn a Django error body ({ field: [msgs] }) into { field: message }. */
function apiErrorMessages(e) {
  const api = e.response?.data;
  const mapped = {};
  if (api && typeof api === "object") {
    Object.entries(api).forEach(([k, v]) => {
      mapped[k] = Array.isArray(v) ? v.join(" ") : String(v);
    });
  }
  return mapped;
}

async function fetchWindows() {
  loadingWindows.value = true;
  try {
    const { data } = await registrationService.listWindows();
    windows.value = data.results || data;
  } catch {
    windows.value = [];
    toast.add({
      severity: "error",
      summary: "Could not load registration windows",
      detail: "Check that the API is running.",
      life: 5000,
    });
  } finally {
    loadingWindows.value = false;
  }
}

async function viewRegistrations(win) {
  activeWindow.value = win;
  loadingRegistrations.value = true;
  try {
    const { data } = await registrationService.listCatechism({ window: win.id });
    registrations.value = data.results || data;
  } catch {
    registrations.value = [];
    toast.add({
      severity: "error",
      summary: "Could not load registrations",
      detail: "Check that the API is running.",
      life: 5000,
    });
  } finally {
    loadingRegistrations.value = false;
  }
}

async function submitCreate() {
  if (!validate()) return;

  creating.value = true;
  try {
    // datetime-local gives "YYYY-MM-DDTHH:mm"; the API expects an ISO string
    const payload = {
      ...form.value,
      opens_at: new Date(form.value.opens_at).toISOString(),
      closes_at: new Date(form.value.closes_at).toISOString(),
    };
    const { data } = await registrationService.createWindow(payload);
    windows.value.unshift(data);
    showCreate.value = false;
    form.value = blank();
    toast.add({ severity: "success", summary: "Registration window created", life: 2500 });
  } catch (e) {
    // Surface Django field errors next to their inputs when we can
    const mapped = apiErrorMessages(e);
    errors.value = { ...errors.value, ...mapped };
    toast.add({
      severity: "error",
      summary: "Could not create window",
      detail: Object.values(mapped)[0] || e.message,
      life: 5000,
    });
  } finally {
    creating.value = false;
  }
}

onMounted(fetchWindows);
</script>
