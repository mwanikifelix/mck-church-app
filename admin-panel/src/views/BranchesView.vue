<template>
  <div>
    <BasePageHeading
      title="Branches"
      icon="fa-map-marker-alt"
      tone="green"
      :subtitle="`${branches.length} recorded`"
    >
      <template #extra>
        <button type="button" class="btn btn-light btn-sm" @click="openCreate">
          <i class="fa fa-plus me-1"></i> New Branch
        </button>
      </template>
    </BasePageHeading>

    <div class="content">
    <AppDataTable
      :rows="branches"
      :columns="columns"
      :loading="loading"
      :page-size="15"
      search-placeholder="Search name, address or description…"
      export-name="branches"
      empty-text="No branches yet. Create the first one."
      empty-icon="fa-map-marker-alt"
    />

    <!-- Create dialog -->
    <AppModal
      v-model:visible="showCreate"
      title="New Branch"
      subtitle="Add a new church branch"
      size="sm"
    >
      <FormField label="Name" required :error="errors.name" field-id="b-name">
        <input
          id="b-name"
          v-model="form.name"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errors.name }"
          placeholder="e.g. MCK Voi Church"
        />
      </FormField>

      <FormField
        label="Short description"
        :error="errors.short_description"
        field-id="b-desc"
        hint="Shown next to the branch in lists"
      >
        <input
          id="b-desc"
          v-model="form.short_description"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errors.short_description }"
          placeholder="e.g. Located near Samburu Primary School"
        />
      </FormField>

      <FormField label="Address" :error="errors.address" field-id="b-address">
        <input
          id="b-address"
          v-model="form.address"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errors.address }"
          placeholder="e.g. P.O. Box 123, Voi"
        />
      </FormField>

      <div class="row g-3">
        <div class="col-12 col-sm-6">
          <FormField label="Latitude" :error="errors.latitude" field-id="b-lat" hint="6 decimal places">
            <input
              id="b-lat"
              v-model.number="form.latitude"
              type="number"
              step="0.000001"
              class="form-control"
              :class="{ 'is-invalid': errors.latitude }"
              placeholder="0.000000"
            />
          </FormField>
        </div>
        <div class="col-12 col-sm-6">
          <FormField label="Longitude" :error="errors.longitude" field-id="b-lng" hint="6 decimal places">
            <input
              id="b-lng"
              v-model.number="form.longitude"
              type="number"
              step="0.000001"
              class="form-control"
              :class="{ 'is-invalid': errors.longitude }"
              placeholder="0.000000"
            />
          </FormField>
        </div>
      </div>

      <FormField
        label="Attendance check-in radius (meters)"
        :error="errors.attendance_radius_meters"
        field-id="b-radius"
      >
        <input
          id="b-radius"
          v-model.number="form.attendance_radius_meters"
          type="number"
          min="0"
          class="form-control"
          :class="{ 'is-invalid': errors.attendance_radius_meters }"
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
          Create branch
        </button>
      </template>
    </AppModal>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "../composables/useToast";
import branchesService from "../services/branches.service";

const toast = useToast();

const branches = ref([]);
const loading = ref(true);
const showCreate = ref(false);
const creating = ref(false);

const columns = [
  { field: "name", header: "Name", sortable: true, strong: true },
  { field: "short_description", header: "Description" },
  { field: "address", header: "Address" },
  { field: "attendance_radius_meters", header: "Check-in Radius (m)", sortable: true },
];

const blank = () => ({
  name: "",
  short_description: "",
  address: "",
  latitude: null,
  longitude: null,
  attendance_radius_meters: 100,
});

const form = ref(blank());
const errors = ref({});

// Empty number inputs come back as "" — send null like the old InputNumber did
const num = (v) => (v === "" ? null : v);

function openCreate() {
  form.value = blank();
  errors.value = {};
  showCreate.value = true;
}

function validate() {
  const e = {};
  if (!form.value.name.trim()) e.name = "Branch name is required.";
  errors.value = e;
  return Object.keys(e).length === 0;
}

async function fetchBranches() {
  loading.value = true;
  try {
    const { data } = await branchesService.list();
    branches.value = data.results || data;
  } catch {
    toast.add({
      severity: "error",
      summary: "Could not load branches",
      detail: "Check that the API is running.",
      life: 5000,
    });
    branches.value = [];
  } finally {
    loading.value = false;
  }
}

async function submitCreate() {
  if (!validate()) return;

  creating.value = true;
  try {
    const payload = {
      ...form.value,
      latitude: num(form.value.latitude),
      longitude: num(form.value.longitude),
      attendance_radius_meters: num(form.value.attendance_radius_meters),
    };
    const { data } = await branchesService.create(payload);
    branches.value.unshift(data);
    showCreate.value = false;
    form.value = blank();
    toast.add({ severity: "success", summary: "Branch created", life: 2500 });
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
        summary: "Could not create branch",
        detail: Object.values(mapped)[0],
        life: 5000,
      });
    } else {
      toast.add({
        severity: "error",
        summary: "Could not create branch",
        detail: e.message,
        life: 5000,
      });
    }
  } finally {
    creating.value = false;
  }
}

onMounted(fetchBranches);
</script>
