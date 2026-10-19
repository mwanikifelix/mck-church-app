<template>
  <div>
    <!-- Header -->
    <div class="header-row mb-3">
      <div>
        <h2 class="section-title mb-0">Departments</h2>
        <p class="text-muted fs-sm mb-0">{{ departments.length }} recorded</p>
      </div>
      <button type="button" class="btn btn-primary btn-sm" @click="openCreate">
        <i class="fa fa-plus me-1"></i> New Department
      </button>
    </div>

    <AppDataTable
      class="mb-4"
      :rows="departments"
      :columns="columns"
      :loading="loadingDepts"
      :page-size="15"
      :search-fields="departmentSearchFields"
      search-placeholder="Search departments…"
      export-name="departments"
      empty-text="No departments yet. Create the first one."
      empty-icon="fa-building"
    >
      <template #meeting="{ row }">
        <span v-if="row.meeting_day || row.meeting_time">
          {{ row.meeting_day }} {{ row.meeting_time }}
        </span>
        <span v-else class="text-muted">—</span>
      </template>
    </AppDataTable>

    <!-- Pending join requests -->
    <h2 class="section-title mb-3">Pending Join Requests</h2>

    <AppDataTable
      :rows="pendingRequests"
      :columns="requestColumns"
      :loading="loadingRequests"
      :page-size="15"
      :search-fields="requestSearchFields"
      search-placeholder="Search requests…"
      empty-text="No pending join requests."
      empty-icon="fa-user-check"
    >
      <template #department="{ row }">
        {{ departmentName(row.department) }}
      </template>

      <template #actions="{ row }">
        <div class="d-flex gap-2 justify-content-end">
          <button
            type="button"
            class="btn btn-success btn-sm"
            :disabled="acting === row.id"
            @click="handle(row, 'approve')"
          >
            <span v-if="acting === row.id" class="spinner-border spinner-border-sm me-1"></span>
            Approve
          </button>
          <button
            type="button"
            class="btn btn-outline-danger btn-sm"
            :disabled="acting === row.id"
            @click="handle(row, 'reject')"
          >
            <span v-if="acting === row.id" class="spinner-border spinner-border-sm me-1"></span>
            Reject
          </button>
        </div>
      </template>
    </AppDataTable>

    <!-- Create dialog -->
    <AppModal
      v-model:visible="showCreate"
      title="New Department"
      subtitle="Add a ministry department"
      size="sm"
    >
      <FormField label="Name" required :error="errors.name" field-id="d-name">
        <input
          id="d-name"
          v-model="form.name"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errors.name }"
          placeholder="e.g. Youth Ministry"
        />
      </FormField>

      <FormField label="Description" :error="errors.description" field-id="d-desc">
        <textarea
          id="d-desc"
          v-model="form.description"
          rows="3"
          class="form-control"
          :class="{ 'is-invalid': errors.description }"
          placeholder="What does this department do?"
        ></textarea>
      </FormField>

      <FormField
        label="Branch"
        :error="errors.branch"
        field-id="d-branch"
        hint="Leave blank for church-wide"
      >
        <select id="d-branch" v-model="form.branch" class="form-select">
          <option :value="null">Church-wide</option>
          <option v-for="b in branches" :key="b.id" :value="b.id">
            {{ b.name }}
          </option>
        </select>
      </FormField>

      <div class="row g-3">
        <div class="col-12 col-sm-6">
          <FormField label="Meeting day" :error="errors.meeting_day" field-id="d-day">
            <input
              id="d-day"
              v-model="form.meeting_day"
              type="text"
              class="form-control"
              :class="{ 'is-invalid': errors.meeting_day }"
              placeholder="e.g. Tuesday"
            />
          </FormField>
        </div>
        <div class="col-12 col-sm-6">
          <FormField label="Meeting time" :error="errors.meeting_time" field-id="d-time">
            <input
              id="d-time"
              v-model="form.meeting_time"
              type="text"
              class="form-control"
              :class="{ 'is-invalid': errors.meeting_time }"
              placeholder="e.g. 5:30PM"
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
          Create department
        </button>
      </template>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "../composables/useToast";
import churchService from "../services/church.service";
import branchesService from "../services/branches.service";

const toast = useToast();

const departments = ref([]);
const pendingRequests = ref([]);
const branches = ref([]);
const loadingDepts = ref(true);
const loadingRequests = ref(true);
const acting = ref(null);
const showCreate = ref(false);
const creating = ref(false);

const columns = [
  { field: "name", header: "Name", sortable: true, strong: true },
  { field: "leader_name", header: "Leader", sortable: true },
  { header: "Meeting", slot: "meeting" },
];
// The Meeting column has no plain field, so search across its parts explicitly
const departmentSearchFields = ["name", "leader_name", "meeting_day", "meeting_time"];

const requestColumns = [
  { field: "user_name", header: "Member", strong: true },
  { field: "department", header: "Department", slot: "department" },
  { field: "message", header: "Message" },
  { header: "Actions", slot: "actions", align: "end", sortable: false },
];
const requestSearchFields = ["user_name", "message", (r) => departmentName(r.department)];

const blank = () => ({
  name: "",
  description: "",
  branch: null,
  meeting_day: "",
  meeting_time: "",
});

const form = ref(blank());
const errors = ref({});

function departmentName(id) {
  return departments.value.find((d) => d.id === id)?.name || id;
}

function openCreate() {
  form.value = blank();
  errors.value = {};
  showCreate.value = true;
}

function validate() {
  const e = {};
  if (!form.value.name.trim()) e.name = "Department name is required.";
  errors.value = e;
  return Object.keys(e).length === 0;
}

async function fetchDepartments() {
  loadingDepts.value = true;
  try {
    const { data } = await churchService.listDepartments();
    departments.value = data.results || data;
  } finally {
    loadingDepts.value = false;
  }
}

async function fetchRequests() {
  loadingRequests.value = true;
  try {
    const { data } = await churchService.listJoinRequests({ status: "pending" });
    pendingRequests.value = data.results || data;
  } finally {
    loadingRequests.value = false;
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

async function handle(request, action) {
  acting.value = request.id;
  try {
    if (action === "approve") await churchService.approveJoinRequest(request.id);
    else await churchService.rejectJoinRequest(request.id);
    pendingRequests.value = pendingRequests.value.filter((r) => r.id !== request.id);
    toast.add({ severity: "success", summary: `Request ${action}d`, life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Action failed", detail: e.response?.data?.detail, life: 3000 });
  } finally {
    acting.value = null;
  }
}

async function submitCreate() {
  if (!validate()) return;

  creating.value = true;
  try {
    const { data } = await churchService.createDepartment(form.value);
    departments.value.unshift(data);
    showCreate.value = false;
    form.value = blank();
    toast.add({ severity: "success", summary: "Department created", life: 2500 });
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
        summary: "Could not create department",
        detail: Object.values(mapped)[0],
        life: 5000,
      });
    } else {
      toast.add({
        severity: "error",
        summary: "Could not create department",
        detail: e.message,
        life: 5000,
      });
    }
  } finally {
    creating.value = false;
  }
}

onMounted(() => {
  fetchDepartments();
  fetchRequests();
  fetchBranches();
});
</script>
