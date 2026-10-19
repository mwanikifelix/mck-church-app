<template>
  <div>
    <BasePageHeading
      title="Events"
      icon="fa-calendar-alt"
      :subtitle="`${events.length} recorded`"
    >
      <template #extra>
        <button type="button" class="btn btn-light btn-sm" @click="openCreate">
          <i class="fa fa-plus me-1"></i> New Event
        </button>
      </template>
    </BasePageHeading>

    <div class="content">
    <AppDataTable
      :rows="events"
      :columns="columns"
      :loading="loading"
      :page-size="15"
      search-placeholder="Search title or location…"
      export-name="events"
      empty-text="No events yet. Create the first one."
      empty-icon="fa-calendar-alt"
    >
      <template #start="{ row }">
        <span v-if="row.start_time">{{ new Date(row.start_time).toLocaleString() }}</span>
        <span v-else class="text-muted">—</span>
      </template>
    </AppDataTable>

    <!-- Create dialog -->
    <AppModal
      v-model:visible="showCreate"
      title="New Event"
      subtitle="Schedule a church event"
      size="sm"
    >
      <FormField label="Title" required :error="errors.title" field-id="e-title">
        <input
          id="e-title"
          v-model="form.title"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errors.title }"
          placeholder="e.g. Youth Convention 2026"
        />
      </FormField>

      <FormField label="Description" :error="errors.description" field-id="e-desc">
        <textarea
          id="e-desc"
          v-model="form.description"
          rows="2"
          class="form-control"
          :class="{ 'is-invalid': errors.description }"
          placeholder="What is this event about?"
        ></textarea>
      </FormField>

      <FormField label="Location" :error="errors.location" field-id="e-location">
        <input
          id="e-location"
          v-model="form.location"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errors.location }"
          placeholder="e.g. MCK Voi Main Church"
        />
      </FormField>

      <div class="row g-3">
        <div class="col-12 col-sm-6">
          <FormField label="Start time" required :error="errors.start_time" field-id="e-start">
            <input
              id="e-start"
              v-model="form.start_time"
              type="datetime-local"
              class="form-control"
              :class="{ 'is-invalid': errors.start_time }"
            />
          </FormField>
        </div>
        <div class="col-12 col-sm-6">
          <FormField label="End time" :error="errors.end_time" field-id="e-end">
            <input
              id="e-end"
              v-model="form.end_time"
              type="datetime-local"
              class="form-control"
              :class="{ 'is-invalid': errors.end_time }"
            />
          </FormField>
        </div>
      </div>

      <FormField
        label="Branch"
        :error="errors.branch"
        field-id="e-branch"
        hint="Leave blank for church-wide"
      >
        <select id="e-branch" v-model="form.branch" class="form-select">
          <option :value="null">Church-wide</option>
          <option v-for="b in branches" :key="b.id" :value="b.id">
            {{ b.name }}
          </option>
        </select>
      </FormField>

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
          Create event
        </button>
      </template>
    </AppModal>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "../composables/useToast";
import eventsService from "../services/events.service";
import branchesService from "../services/branches.service";

const toast = useToast();

const events = ref([]);
const branches = ref([]);
const loading = ref(true);
const showCreate = ref(false);
const creating = ref(false);

const columns = [
  { field: "title", header: "Title", sortable: true, strong: true },
  { field: "start_time", header: "Start", sortable: true, slot: "start" },
  { field: "location", header: "Location" },
  { field: "rsvp_count", header: "RSVPs", sortable: true },
];

const blank = () => ({
  title: "",
  description: "",
  location: "",
  start_time: "",
  end_time: "",
  branch: null,
});

const form = ref(blank());
const errors = ref({});

function openCreate() {
  form.value = blank();
  errors.value = {};
  showCreate.value = true;
}

function validate() {
  const e = {};
  if (!form.value.title.trim()) e.title = "Event title is required.";
  if (!form.value.start_time) e.start_time = "Start time is required.";
  if (form.value.end_time && form.value.start_time && form.value.end_time <= form.value.start_time)
    e.end_time = "End time must be after the start time.";
  errors.value = e;
  return Object.keys(e).length === 0;
}

async function fetchEvents() {
  loading.value = true;
  try {
    const { data } = await eventsService.list();
    events.value = data.results || data;
  } catch {
    toast.add({
      severity: "error",
      summary: "Could not load events",
      detail: "Check that the API is running.",
      life: 5000,
    });
    events.value = [];
  } finally {
    loading.value = false;
  }
}

async function fetchBranches() {
  try {
    const { data } = await branchesService.list();
    branches.value = data.results || data;
  } catch {
    branches.value = [];
  }
}

async function submitCreate() {
  if (!validate()) return;

  creating.value = true;
  try {
    // datetime-local gives "YYYY-MM-DDTHH:mm" strings; the API expects ISO 8601
    const payload = {
      ...form.value,
      start_time: form.value.start_time
        ? new Date(form.value.start_time).toISOString()
        : undefined,
      end_time: form.value.end_time ? new Date(form.value.end_time).toISOString() : null,
    };
    const { data } = await eventsService.create(payload);
    events.value.unshift(data);
    showCreate.value = false;
    form.value = blank();
    toast.add({ severity: "success", summary: "Event created", life: 2500 });
  } catch (e) {
    // Surface Django field errors next to their inputs when we can
    const api = e.response?.data;
    if (api && typeof api === "object") {
      const mapped = {};
      Object.entries(api).forEach(([k, v]) => {
        mapped[k] = Array.isArray(v) ? v.join(" ") : String(v);
      });
      errors.value = { ...errors.value, ...mapped };
      toast.add({
        severity: "error",
        summary: "Could not create event",
        detail: Object.values(mapped)[0],
        life: 5000,
      });
    } else {
      toast.add({
        severity: "error",
        summary: "Could not create event",
        detail: e.message,
        life: 5000,
      });
    }
  } finally {
    creating.value = false;
  }
}

onMounted(() => {
  fetchEvents();
  fetchBranches();
});
</script>
