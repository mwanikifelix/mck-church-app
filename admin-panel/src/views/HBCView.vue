<template>
  <div>
    <div class="header-row">
      <h2 class="section-title">HBC Groups</h2>
      <Button label="New HBC Group" icon="pi pi-plus" @click="showCreate = true" />
    </div>
    <DataTable :value="groups" :loading="loading" paginator :rows="15" sortMode="multiple">
      <Column field="name" header="Name" sortable />
      <Column field="location" header="Location" sortable />
      <Column field="leader_name" header="Leader" />
      <Column field="member_count" header="Members" sortable />
      <Column header="Total Contributions">
        <template #body="{ data }">{{ data.total_contributions || 0 }}</template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="showCreate" header="New HBC Group" modal style="width:460px">
      <div class="form-field">
        <label>Name</label>
        <InputText v-model="form.name" class="w-full" placeholder="e.g. HBC 12 - Ganjoni" />
      </div>
      <div class="form-field">
        <label>Branch</label>
        <Select v-model="form.branch" :options="branches" optionLabel="name" optionValue="id" class="w-full" placeholder="Select branch" />
      </div>
      <div class="form-field">
        <label>Location</label>
        <InputText v-model="form.location" class="w-full" />
      </div>
      <div class="form-row">
        <div class="form-field">
          <label>Meeting Day</label>
          <InputText v-model="form.meeting_day" class="w-full" placeholder="e.g. Wednesday" />
        </div>
        <div class="form-field">
          <label>Meeting Time</label>
          <InputText v-model="form.meeting_time" class="w-full" placeholder="e.g. 7:00PM" />
        </div>
      </div>
      <div class="form-field">
        <label>Meeting Venue</label>
        <InputText v-model="form.meeting_venue" class="w-full" />
      </div>
      <div class="form-row">
        <div class="form-field">
          <label>Treasurer Name</label>
          <InputText v-model="form.treasurer_name" class="w-full" />
        </div>
        <div class="form-field">
          <label>Treasurer Phone</label>
          <InputText v-model="form.treasurer_phone" class="w-full" />
        </div>
      </div>
      <div class="form-field">
        <label>Subscription Fee</label>
        <InputNumber v-model="form.subscription_fee" class="w-full" mode="decimal" :minFractionDigits="2" />
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
import InputNumber from "primevue/inputnumber";
import Select from "primevue/select";
import { useToast } from "primevue/usetoast";
import hbcService from "../services/hbc.service";
import branchesService from "../services/branches.service";

const toast = useToast();
const groups = ref([]);
const branches = ref([]);
const loading = ref(true);
const showCreate = ref(false);
const creating = ref(false);
const form = ref({
  name: "", branch: null, location: "", meeting_day: "", meeting_time: "",
  meeting_venue: "", treasurer_name: "", treasurer_phone: "", subscription_fee: 0,
});

async function fetchGroups() {
  loading.value = true;
  try {
    const { data } = await hbcService.list();
    groups.value = data.results || data;
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
  creating.value = true;
  try {
    const { data } = await hbcService.create(form.value);
    groups.value.unshift(data);
    showCreate.value = false;
    form.value = {
      name: "", branch: null, location: "", meeting_day: "", meeting_time: "",
      meeting_venue: "", treasurer_name: "", treasurer_phone: "", subscription_fee: 0,
    };
    toast.add({ severity: "success", summary: "HBC group created", life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Failed to create", detail: JSON.stringify(e.response?.data), life: 4000 });
  } finally {
    creating.value = false;
  }
}

onMounted(() => {
  fetchGroups();
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
.w-full { width: 100%; }
</style>
