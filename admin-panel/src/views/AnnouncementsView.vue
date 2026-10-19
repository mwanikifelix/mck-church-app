<template>
  <div>
    <BasePageHeading
      title="Announcements"
      icon="fa-bullhorn"
      :subtitle="`${announcements.length} recorded`"
    >
      <template #extra>
        <button type="button" class="btn btn-light btn-sm" @click="openCreate">
          <i class="fa fa-plus me-1"></i> New Announcement
        </button>
      </template>
    </BasePageHeading>

    <div class="content">
    <AppDataTable
      :rows="announcements"
      :columns="columns"
      :loading="loading"
      :page-size="15"
      search-placeholder="Search announcements…"
      export-name="announcements"
      empty-text="No announcements yet. Publish the first one."
      empty-icon="fa-bullhorn"
    >
      <template #pinned="{ row }">
        <span
          v-if="row.is_pinned"
          class="badge rounded-pill bg-warning-subtle text-warning-emphasis"
        >
          <i class="fa fa-thumbtack me-1"></i> Pinned
        </span>
        <span v-else class="text-muted">—</span>
      </template>
    </AppDataTable>

    <!-- Create dialog -->
    <AppModal
      v-model:visible="showCreate"
      title="New Announcement"
      subtitle="Publish a notice to the church"
      size="sm"
    >
      <FormField label="Title" required :error="errors.title" field-id="a-title">
        <input
          id="a-title"
          v-model="form.title"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errors.title }"
          placeholder="e.g. Sunday Service Moved to 9AM"
        />
      </FormField>

      <FormField label="Body" required :error="errors.body" field-id="a-body">
        <textarea
          id="a-body"
          v-model="form.body"
          rows="4"
          class="form-control"
          :class="{ 'is-invalid': errors.body }"
          placeholder="Write the announcement…"
        ></textarea>
      </FormField>

      <FormField
        label="Branch"
        :error="errors.branch"
        field-id="a-branch"
        hint="Leave blank for church-wide"
      >
        <select id="a-branch" v-model="form.branch" class="form-select">
          <option :value="null">Church-wide</option>
          <option v-for="b in branches" :key="b.id" :value="b.id">
            {{ b.name }}
          </option>
        </select>
      </FormField>

      <div class="form-check mb-3">
        <input
          id="a-pinned"
          v-model="form.is_pinned"
          type="checkbox"
          class="form-check-input"
        />
        <label class="form-check-label" for="a-pinned">Pin to top</label>
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
          Publish
        </button>
      </template>
    </AppModal>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "../composables/useToast";
import contentService from "../services/content.service";
import branchesService from "../services/branches.service";

const toast = useToast();

const announcements = ref([]);
const branches = ref([]);
const loading = ref(true);
const showCreate = ref(false);
const creating = ref(false);

const columns = [
  { field: "title", header: "Title", sortable: true, strong: true },
  { field: "body", header: "Body" },
  { field: "is_pinned", header: "Pinned", slot: "pinned" },
];

const blank = () => ({ title: "", body: "", branch: null, is_pinned: false });

const form = ref(blank());
const errors = ref({});

function openCreate() {
  form.value = blank();
  errors.value = {};
  showCreate.value = true;
}

function validate() {
  const e = {};
  if (!form.value.title.trim()) e.title = "Title is required.";
  if (!form.value.body.trim()) e.body = "Announcement body is required.";
  errors.value = e;
  return Object.keys(e).length === 0;
}

async function fetchAnnouncements() {
  loading.value = true;
  try {
    const { data } = await contentService.listAnnouncements();
    announcements.value = data.results || data;
  } catch {
    toast.add({
      severity: "error",
      summary: "Could not load announcements",
      detail: "Check that the API is running.",
      life: 5000,
    });
    announcements.value = [];
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
    const { data } = await contentService.createAnnouncement(form.value);
    announcements.value.unshift(data);
    showCreate.value = false;
    form.value = blank();
    toast.add({ severity: "success", summary: "Announcement published", life: 2500 });
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
        summary: "Could not publish announcement",
        detail: Object.values(mapped)[0],
        life: 5000,
      });
    } else {
      toast.add({
        severity: "error",
        summary: "Could not publish announcement",
        detail: e.message,
        life: 5000,
      });
    }
  } finally {
    creating.value = false;
  }
}

onMounted(() => {
  fetchAnnouncements();
  fetchBranches();
});
</script>
