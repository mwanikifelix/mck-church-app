<template>
  <div>
    <!-- Header -->
    <div class="header-row mb-3">
      <div>
        <h2 class="section-title mb-0">HBC Groups</h2>
        <p class="text-muted fs-sm mb-0">
          {{ groups.length }} {{ groups.length === 1 ? "group" : "groups" }}
        </p>
      </div>
      <button type="button" class="btn btn-primary btn-sm" @click="openCreate">
        <i class="fa fa-plus me-1"></i> New HBC Group
      </button>
    </div>

    <AppDataTable
      :rows="groups"
      :columns="columns"
      :loading="loading"
      :page-size="15"
      search-placeholder="Search name, location or leader…"
      export-name="hbc-groups"
      empty-text="No HBC groups yet. Create the first one."
      empty-icon="fa-home"
    >
      <template #contributions="{ value }">
        {{ value || 0 }}
      </template>
    </AppDataTable>

    <!-- Create dialog -->
    <AppModal
      v-model:visible="showCreate"
      title="New HBC Group"
      subtitle="Register a home-based church cell"
      size="sm"
    >
      <FormField label="Name" required :error="errors.name" field-id="h-name">
        <input
          id="h-name"
          v-model="form.name"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errors.name }"
          placeholder="e.g. HBC 12 - Ganjoni"
        />
      </FormField>

      <FormField label="Branch" :error="errors.branch" field-id="h-branch">
        <select id="h-branch" v-model="form.branch" class="form-select">
          <option :value="null">Select branch</option>
          <option v-for="b in branches" :key="b.id" :value="b.id">
            {{ b.name }}
          </option>
        </select>
      </FormField>

      <FormField label="Location" :error="errors.location" field-id="h-location">
        <input
          id="h-location"
          v-model="form.location"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errors.location }"
          placeholder="e.g. Ganjoni, Mombasa"
        />
      </FormField>

      <div class="row g-3">
        <div class="col-12 col-sm-6">
          <FormField label="Meeting day" :error="errors.meeting_day" field-id="h-day">
            <input
              id="h-day"
              v-model="form.meeting_day"
              type="text"
              class="form-control"
              :class="{ 'is-invalid': errors.meeting_day }"
              placeholder="e.g. Wednesday"
            />
          </FormField>
        </div>
        <div class="col-12 col-sm-6">
          <FormField label="Meeting time" :error="errors.meeting_time" field-id="h-time">
            <input
              id="h-time"
              v-model="form.meeting_time"
              type="text"
              class="form-control"
              :class="{ 'is-invalid': errors.meeting_time }"
              placeholder="e.g. 7:00PM"
            />
          </FormField>
        </div>
      </div>

      <FormField label="Meeting venue" :error="errors.meeting_venue" field-id="h-venue">
        <input
          id="h-venue"
          v-model="form.meeting_venue"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errors.meeting_venue }"
        />
      </FormField>

      <div class="row g-3">
        <div class="col-12 col-sm-6">
          <FormField
            label="Treasurer name"
            :error="errors.treasurer_name"
            field-id="h-treasurer"
          >
            <input
              id="h-treasurer"
              v-model="form.treasurer_name"
              type="text"
              class="form-control"
              :class="{ 'is-invalid': errors.treasurer_name }"
            />
          </FormField>
        </div>
        <div class="col-12 col-sm-6">
          <FormField
            label="Treasurer phone"
            :error="errors.treasurer_phone"
            field-id="h-phone"
          >
            <input
              id="h-phone"
              v-model="form.treasurer_phone"
              type="tel"
              class="form-control"
              :class="{ 'is-invalid': errors.treasurer_phone }"
              placeholder="e.g. 0712345678"
            />
          </FormField>
        </div>
      </div>

      <FormField
        label="Subscription fee"
        :error="errors.subscription_fee"
        field-id="h-fee"
        hint="Amount due per member per month"
      >
        <input
          id="h-fee"
          v-model.number="form.subscription_fee"
          type="number"
          min="0"
          step="0.01"
          class="form-control"
          :class="{ 'is-invalid': errors.subscription_fee }"
        />
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
          Create group
        </button>
      </template>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "../composables/useToast";
import hbcService from "../services/hbc.service";
import branchesService from "../services/branches.service";

const toast = useToast();

const groups = ref([]);
const branches = ref([]);
const loading = ref(true);
const showCreate = ref(false);
const creating = ref(false);

const columns = [
  { field: "name", header: "Name", sortable: true, strong: true },
  { field: "location", header: "Location", sortable: true },
  { field: "leader_name", header: "Leader" },
  { field: "member_count", header: "Members", sortable: true },
  { field: "total_contributions", header: "Total Contributions", slot: "contributions" },
];

const blank = () => ({
  name: "",
  branch: null,
  location: "",
  meeting_day: "",
  meeting_time: "",
  meeting_venue: "",
  treasurer_name: "",
  treasurer_phone: "",
  subscription_fee: 0,
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

  const fee = Number(form.value.subscription_fee);
  if (form.value.subscription_fee === "" || Number.isNaN(fee))
    e.subscription_fee = "Enter a subscription fee.";
  else if (fee < 0) e.subscription_fee = "Fee cannot be negative.";

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

async function fetchGroups() {
  loading.value = true;
  try {
    const { data } = await hbcService.list();
    groups.value = data.results || data;
  } catch {
    groups.value = [];
    toast.add({
      severity: "error",
      summary: "Could not load HBC groups",
      detail: "Check that the API is running.",
      life: 5000,
    });
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
    const { data } = await hbcService.create(form.value);
    groups.value.unshift(data);
    showCreate.value = false;
    form.value = blank();
    toast.add({ severity: "success", summary: "HBC group created", life: 2500 });
  } catch (e) {
    // Surface Django field errors next to their inputs when we can
    const mapped = apiErrorMessages(e);
    errors.value = { ...errors.value, ...mapped };
    toast.add({
      severity: "error",
      summary: "Could not create HBC group",
      detail: Object.values(mapped)[0] || e.message,
      life: 5000,
    });
  } finally {
    creating.value = false;
  }
}

onMounted(() => {
  fetchGroups();
  fetchBranches();
});
</script>
