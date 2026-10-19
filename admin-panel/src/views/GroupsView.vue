<template>
  <div>
    <BasePageHeading
      title="Growth-Track Groups"
      icon="fa-project-diagram"
      tone="green"
      :subtitle="`${store.items.length} ${store.items.length === 1 ? 'group' : 'groups'}`"
    >
      <template #extra>
        <button type="button" class="btn btn-light btn-sm" @click="openCreate">
          <i class="fa fa-plus me-1"></i> New Group
        </button>
      </template>
    </BasePageHeading>

    <div class="content">
    <AppDataTable
      :rows="store.items"
      :columns="columns"
      :loading="store.loading"
      :page-size="15"
      search-placeholder="Search name, branch or age range…"
      export-name="groups"
      empty-text="No groups yet. Create the first one."
      empty-icon="fa-project-diagram"
    >
      <template #branch="{ row }">
        <span v-if="row.branch_name" class="badge rounded-pill bg-light text-dark border">
          {{ row.branch_name }}
        </span>
        <span v-else class="text-muted">—</span>
      </template>

      <template #age="{ row }">{{ row.min_age }} - {{ row.max_age }}</template>

      <template #active="{ row }">
        <span
          class="badge rounded-pill"
          :class="
            row.is_active
              ? 'bg-success-subtle text-success-emphasis'
              : 'bg-secondary-subtle text-secondary-emphasis'
          "
        >
          {{ row.is_active ? "Yes" : "No" }}
        </span>
      </template>
    </AppDataTable>

    <!-- Create dialog -->
    <AppModal
      v-model:visible="showCreate"
      title="New Growth-Track Group"
      subtitle="Set up a discipleship group and its eligibility rules"
      size="sm"
    >
      <FormField label="Name" required :error="errors.name" field-id="g-name">
        <input
          id="g-name"
          v-model="form.name"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errors.name }"
          placeholder="e.g. Youth - Wesley Mombasa"
        />
      </FormField>

      <FormField label="Branch" required :error="errors.branch" field-id="g-branch">
        <select
          id="g-branch"
          v-model="form.branch"
          class="form-select"
          :class="{ 'is-invalid': errors.branch }"
        >
          <option :value="null">Select branch</option>
          <option v-for="b in branches" :key="b.id" :value="b.id">
            {{ b.name }}
          </option>
        </select>
      </FormField>

      <FormField label="Description" :error="errors.description" field-id="g-desc">
        <textarea
          id="g-desc"
          v-model="form.description"
          rows="2"
          class="form-control"
          :class="{ 'is-invalid': errors.description }"
          placeholder="What is this group about?"
        ></textarea>
      </FormField>

      <div class="row g-3">
        <div class="col-12 col-sm-6">
          <FormField label="Min age" required :error="errors.min_age" field-id="g-min-age">
            <input
              id="g-min-age"
              v-model.number="form.min_age"
              type="number"
              min="0"
              class="form-control"
              :class="{ 'is-invalid': errors.min_age }"
            />
          </FormField>
        </div>
        <div class="col-12 col-sm-6">
          <FormField label="Max age" required :error="errors.max_age" field-id="g-max-age">
            <input
              id="g-max-age"
              v-model.number="form.max_age"
              type="number"
              min="0"
              class="form-control"
              :class="{ 'is-invalid': errors.max_age }"
            />
          </FormField>
        </div>
      </div>

      <FormField
        label="Marital status requirement"
        :error="errors.marital_status_requirement"
        field-id="g-marital"
      >
        <select id="g-marital" v-model="form.marital_status_requirement" class="form-select">
          <option v-for="m in maritalOptions" :key="m.value" :value="m.value">
            {{ m.label }}
          </option>
        </select>
      </FormField>

      <div class="form-check mb-3">
        <input
          id="g-enforce"
          v-model="form.enforce_eligibility"
          type="checkbox"
          class="form-check-input"
        />
        <label class="form-check-label" for="g-enforce">
          Enforce age/marital eligibility on join
        </label>
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
          Create group
        </button>
      </template>
    </AppModal>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "../composables/useToast";
import { useGroupsStore } from "../store/groups";
import groupsService from "../services/groups.service";
import branchesService from "../services/branches.service";

const toast = useToast();

const store = useGroupsStore();
const branches = ref([]);
const showCreate = ref(false);
const creating = ref(false);

const maritalOptions = [
  { label: "Any", value: "any" },
  { label: "Single only", value: "single" },
  { label: "Married only", value: "married" },
];

const columns = [
  { field: "name", header: "Name", sortable: true, strong: true },
  { field: "branch_name", header: "Branch", slot: "branch" },
  { field: "min_age", header: "Age Range", slot: "age" },
  { field: "is_active", header: "Active", slot: "active" },
];

const blank = () => ({
  name: "",
  branch: null,
  description: "",
  min_age: 0,
  max_age: 120,
  marital_status_requirement: "any",
  enforce_eligibility: false,
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
  if (!form.value.name.trim()) e.name = "Group name is required.";
  if (!form.value.branch) e.branch = "Branch is required.";

  const min = Number(form.value.min_age);
  const max = Number(form.value.max_age);
  if (form.value.min_age === "" || Number.isNaN(min) || min < 0)
    e.min_age = "Enter a minimum age of 0 or more.";
  else if (form.value.max_age === "" || Number.isNaN(max))
    e.max_age = "Enter a maximum age.";
  else if (max < min)
    e.max_age = "Maximum age must be greater than or equal to minimum age.";

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
    const { data } = await groupsService.create(form.value);
    store.items.unshift(data);
    showCreate.value = false;
    form.value = blank();
    toast.add({ severity: "success", summary: "Group created", life: 2500 });
  } catch (e) {
    // Surface Django field errors next to their inputs when we can
    const mapped = apiErrorMessages(e);
    errors.value = { ...errors.value, ...mapped };
    toast.add({
      severity: "error",
      summary: "Could not create group",
      detail: Object.values(mapped)[0] || e.message,
      life: 5000,
    });
  } finally {
    creating.value = false;
  }
}

onMounted(() => {
  store.fetchAll().catch(() => {
    toast.add({
      severity: "error",
      summary: "Could not load groups",
      detail: "Check that the API is running.",
      life: 5000,
    });
  });
  fetchBranches();
});
</script>
