<template>
  <div>
    <BasePageHeading
      title="Members"
      icon="fa-users"
      :subtitle="`${members.length} registered ${members.length === 1 ? 'member' : 'members'}`"
    >
      <template #extra>
        <button
          v-if="$can('members.view_all')"
          type="button"
          class="btn btn-light btn-sm"
          @click="openCreate"
        >
          <i class="fa fa-plus me-1"></i> New Member
        </button>
      </template>
    </BasePageHeading>

    <div class="content">
    <AppDataTable
      :rows="members"
      :columns="columns"
      :loading="loading"
      :page-size="15"
      search-placeholder="Search name, email or membership no…"
      export-name="members"
      empty-text="No members yet. Create the first one."
      empty-icon="fa-users"
    >
      <template #branch="{ row }">
        <span v-if="row.branch?.name" class="badge rounded-pill bg-light text-dark border">
          {{ row.branch.name }}
        </span>
        <span v-else class="text-muted">—</span>
      </template>

      <template #status="{ row }">
        <span class="badge rounded-pill" :class="statusClass(row.status)">
          <i class="fa fa-circle me-1" style="font-size: 0.5rem; vertical-align: middle"></i>
          {{ row.status || "unknown" }}
        </span>
      </template>
    </AppDataTable>

    <!-- Create dialog -->
    <AppModal
      v-model:visible="showCreate"
      title="New Member"
      subtitle="Add a member to the church register"
      size="sm"
    >
      <FormField label="Full name" required :error="errors.full_name" field-id="m-full-name">
        <input
          id="m-full-name"
          v-model="form.full_name"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errors.full_name }"
          placeholder="e.g. Jane Wanjiku"
          autocomplete="name"
        />
      </FormField>

      <FormField label="Email" required :error="errors.email" field-id="m-email" hint="Used to sign in">
        <input
          id="m-email"
          v-model="form.email"
          type="email"
          class="form-control"
          :class="{ 'is-invalid': errors.email }"
          placeholder="name@example.com"
          autocomplete="email"
        />
      </FormField>

      <FormField label="Branch" :error="errors.branch" field-id="m-branch">
        <select id="m-branch" v-model="form.branch" class="form-select">
          <option :value="null">Unassigned</option>
          <option v-for="b in branches" :key="b.id" :value="b.id">
            {{ b.name }}
          </option>
        </select>
      </FormField>

      <div class="row g-3">
        <div class="col-12 col-sm-6">
          <FormField label="Temporary password" required :error="errors.password" field-id="m-pass">
            <input
              id="m-pass"
              v-model="form.password"
              type="password"
              class="form-control"
              :class="{ 'is-invalid': errors.password }"
              autocomplete="new-password"
            />
          </FormField>
        </div>
        <div class="col-12 col-sm-6">
          <FormField label="Confirm password" required :error="errors.confirm_password" field-id="m-pass2">
            <input
              id="m-pass2"
              v-model="form.confirm_password"
              type="password"
              class="form-control"
              :class="{ 'is-invalid': errors.confirm_password }"
              autocomplete="new-password"
            />
          </FormField>
        </div>
      </div>

      <div class="alert alert-light py-2 fs-sm mb-0 d-flex align-items-start gap-2">
        <i class="fa fa-info-circle mt-1"></i>
        <span>The member can change this password later from their own account.</span>
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
          Create member
        </button>
      </template>
    </AppModal>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "../composables/useToast";
import membersService from "../services/members.service";
import branchesService from "../services/branches.service";

const toast = useToast();

const members = ref([]);
const branches = ref([]);
const loading = ref(true);
const showCreate = ref(false);
const creating = ref(false);

const columns = [
  { field: "full_name", header: "Name", sortable: true, strong: true },
  { field: "email", header: "Email", sortable: true },
  { field: "membership_number", header: "Membership No.", sortable: true, below: "xl" },
  { field: "branch", header: "Branch", slot: "branch" },
  { field: "status", header: "Status", slot: "status" },
];

const blank = () => ({
  full_name: "",
  email: "",
  branch: null,
  password: "",
  confirm_password: "",
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
  if (!form.value.full_name.trim()) e.full_name = "Full name is required.";
  if (!form.value.email.trim()) e.email = "Email is required.";
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email.trim()))
    e.email = "Enter a valid email address.";
  if (!form.value.password) e.password = "Password is required.";
  else if (form.value.password.length < 6) e.password = "At least 6 characters.";
  if (form.value.password !== form.value.confirm_password)
    e.confirm_password = "Passwords do not match.";

  errors.value = e;
  return Object.keys(e).length === 0;
}

function statusClass(status) {
  if (status === "active") return "bg-success-subtle text-success-emphasis";
  if (status === "inactive") return "bg-warning-subtle text-warning-emphasis";
  if (status === "transferred") return "bg-info-subtle text-info-emphasis";
  return "bg-secondary-subtle text-secondary-emphasis";
}

async function fetchMembers() {
  loading.value = true;
  try {
    const { data } = await membersService.list();
    members.value = data.results || data;
  } catch {
    toast.add({
      severity: "error",
      summary: "Could not load members",
      detail: "Check that the API is running.",
      life: 5000,
    });
    members.value = [];
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
    await membersService.create(form.value);
    showCreate.value = false;
    toast.add({ severity: "success", summary: "Member created", life: 2500 });
    fetchMembers();
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
        summary: "Could not create member",
        detail: Object.values(mapped)[0],
        life: 5000,
      });
    } else {
      toast.add({
        severity: "error",
        summary: "Could not create member",
        detail: e.message,
        life: 5000,
      });
    }
  } finally {
    creating.value = false;
  }
}

onMounted(() => {
  fetchMembers();
  fetchBranches();
});
</script>
