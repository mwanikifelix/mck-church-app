<template>
  <div>
    <div class="header-row">
      <h2 class="section-title">Members</h2>
      <Button label="New Member" icon="pi pi-plus" @click="showCreate = true" />
    </div>
    <DataTable
      :value="members"
      :loading="loading"
      paginator
      :rows="15"
      :globalFilterFields="['full_name', 'email', 'membership_number']"
      v-model:filters="filters"
      filterDisplay="menu"
      sortMode="multiple"
    >
      <template #header>
        <div style="display:flex; justify-content:flex-end;">
          <IconField>
            <InputIcon class="pi pi-search" />
            <InputText v-model="filters.global.value" placeholder="Search members..." />
          </IconField>
        </div>
      </template>
      <Column field="full_name" header="Name" sortable />
      <Column field="email" header="Email" sortable />
      <Column field="membership_number" header="Membership No." sortable />
      <Column header="Branch">
        <template #body="{ data }">{{ data.branch?.name || "-" }}</template>
      </Column>
      <Column field="status" header="Status" sortable>
        <template #body="{ data }">
          <Tag :value="data.status" :severity="statusSeverity(data.status)" />
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="showCreate" header="New Member" modal style="width:460px">
      <div class="form-field">
        <label>Full Name</label>
        <InputText v-model="form.full_name" class="w-full" />
      </div>
      <div class="form-field">
        <label>Email</label>
        <InputText v-model="form.email" type="email" class="w-full" />
      </div>
      <div class="form-field">
        <label>Branch</label>
        <Select v-model="form.branch" :options="branches" optionLabel="name" optionValue="id" class="w-full" showClear placeholder="Unassigned" />
      </div>
      <div class="form-row">
        <div class="form-field">
          <label>Temporary Password</label>
          <Password v-model="form.password" :feedback="false" toggleMask class="w-full" inputClass="w-full" />
        </div>
        <div class="form-field">
          <label>Confirm Password</label>
          <Password v-model="form.confirm_password" :feedback="false" toggleMask class="w-full" inputClass="w-full" />
        </div>
      </div>
      <Message severity="info" :closable="false" class="mb-2">
        The member can change this password later from their own account.
      </Message>
      <template #footer>
        <Button label="Cancel" text @click="showCreate = false" />
        <Button label="Create" :loading="creating" @click="submitCreate" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import InputText from "primevue/inputtext";
import IconField from "primevue/iconfield";
import InputIcon from "primevue/inputicon";
import Tag from "primevue/tag";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import Select from "primevue/select";
import Password from "primevue/password";
import Message from "primevue/message";
import { FilterMatchMode } from "@primevue/core/api";
import { useToast } from "primevue/usetoast";
import membersService from "../services/members.service";
import branchesService from "../services/branches.service";

const toast = useToast();
const members = ref([]);
const branches = ref([]);
const loading = ref(true);
const showCreate = ref(false);
const creating = ref(false);
const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
});
const form = ref({ full_name: "", email: "", branch: null, password: "", confirm_password: "" });

async function fetchMembers() {
  loading.value = true;
  try {
    const { data } = await membersService.list();
    members.value = data.results || data;
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

function statusSeverity(status) {
  if (status === "active") return "success";
  if (status === "inactive") return "warn";
  if (status === "transferred") return "info";
  return "secondary";
}

async function submitCreate() {
  creating.value = true;
  try {
    await membersService.create(form.value);
    showCreate.value = false;
    form.value = { full_name: "", email: "", branch: null, password: "", confirm_password: "" };
    toast.add({ severity: "success", summary: "Member created", life: 2500 });
    fetchMembers();
  } catch (e) {
    toast.add({ severity: "error", summary: "Failed to create", detail: JSON.stringify(e.response?.data), life: 4000 });
  } finally {
    creating.value = false;
  }
}

onMounted(() => {
  fetchMembers();
  fetchBranches();
});
</script>

<style scoped>
.section-title { font-size: 1.1rem; font-weight: 600; margin: 0; color: #1e293b; }
.header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.form-field { margin-bottom: 1rem; }
.form-field label { display: block; margin-bottom: 0.35rem; font-size: 0.85rem; color: #475569; }
.form-row { display: flex; gap: 1rem; }
.form-row .form-field { flex: 1; }
.mb-2 { margin-bottom: 1rem; }
.w-full { width: 100%; }
</style>
