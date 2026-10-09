<template>
  <div>
    <div class="header-row">
      <h2 class="section-title">Departments</h2>
      <Button label="New Department" icon="pi pi-plus" @click="showCreate = true" />
    </div>
    <DataTable :value="departments" :loading="loadingDepts" paginator :rows="10" class="mb-4">
      <Column field="name" header="Name" sortable />
      <Column field="leader_name" header="Leader" />
      <Column header="Meeting">
        <template #body="{ data }">{{ data.meeting_day }} {{ data.meeting_time }}</template>
      </Column>
    </DataTable>

    <h2 class="section-title">Pending Join Requests</h2>
    <DataTable :value="pendingRequests" :loading="loadingRequests" paginator :rows="10">
      <template #empty>No pending join requests.</template>
      <Column header="Member"><template #body="{ data }">{{ data.user_name }}</template></Column>
      <Column header="Department"><template #body="{ data }">{{ departmentName(data.department) }}</template></Column>
      <Column field="message" header="Message" />
      <Column header="Actions">
        <template #body="{ data }">
          <Button label="Approve" size="small" severity="success" class="mr-2" :loading="acting === data.id" @click="handle(data, 'approve')" />
          <Button label="Reject" size="small" severity="danger" outlined :loading="acting === data.id" @click="handle(data, 'reject')" />
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="showCreate" header="New Department" modal style="width:420px">
      <div class="form-field">
        <label>Name</label>
        <InputText v-model="form.name" class="w-full" />
      </div>
      <div class="form-field">
        <label>Description</label>
        <Textarea v-model="form.description" class="w-full" rows="3" />
      </div>
      <div class="form-field">
        <label>Branch (leave blank for church-wide)</label>
        <Select v-model="form.branch" :options="branches" optionLabel="name" optionValue="id" class="w-full" showClear placeholder="Church-wide" />
      </div>
      <div class="form-row">
        <div class="form-field">
          <label>Meeting Day</label>
          <InputText v-model="form.meeting_day" class="w-full" placeholder="e.g. Tuesday" />
        </div>
        <div class="form-field">
          <label>Meeting Time</label>
          <InputText v-model="form.meeting_time" class="w-full" placeholder="e.g. 5:30PM" />
        </div>
      </div>
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
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import Select from "primevue/select";
import { useToast } from "primevue/usetoast";
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
const form = ref({ name: "", description: "", branch: null, meeting_day: "", meeting_time: "" });

function departmentName(id) {
  return departments.value.find((d) => d.id === id)?.name || id;
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
  creating.value = true;
  try {
    const { data } = await churchService.createDepartment(form.value);
    departments.value.unshift(data);
    showCreate.value = false;
    form.value = { name: "", description: "", branch: null, meeting_day: "", meeting_time: "" };
    toast.add({ severity: "success", summary: "Department created", life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Failed to create", detail: JSON.stringify(e.response?.data), life: 4000 });
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

<style scoped>
.section-title { font-size: 1.1rem; font-weight: 600; margin: 0 0 0.75rem; color: #1e293b; }
.header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.mb-4 { margin-bottom: 2rem; }
.mr-2 { margin-right: 0.5rem; }
.form-field { margin-bottom: 1rem; }
.form-field label { display: block; margin-bottom: 0.35rem; font-size: 0.85rem; color: #475569; }
.form-row { display: flex; gap: 1rem; }
.form-row .form-field { flex: 1; }
.w-full { width: 100%; }
</style>
