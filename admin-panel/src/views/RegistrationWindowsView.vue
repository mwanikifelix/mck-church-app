<template>
  <div>
    <div class="header-row">
      <h2 class="section-title">Registration Windows</h2>
      <Button label="New Window" icon="pi pi-plus" @click="showCreate = true" />
    </div>
    <DataTable :value="windows" :loading="loadingWindows" paginator :rows="10" class="mb-4">
      <Column field="name" header="Name" sortable />
      <Column header="Opens">
        <template #body="{ data }">{{ new Date(data.opens_at).toLocaleString() }}</template>
      </Column>
      <Column header="Closes">
        <template #body="{ data }">{{ new Date(data.closes_at).toLocaleString() }}</template>
      </Column>
      <Column header="Status">
        <template #body="{ data }">
          <Tag :value="data.is_open ? 'Open' : 'Closed'" :severity="data.is_open ? 'success' : 'secondary'" />
        </template>
      </Column>
      <Column header="">
        <template #body="{ data }">
          <Button label="View Registrations" size="small" text @click="viewRegistrations(data)" />
        </template>
      </Column>
    </DataTable>

    <h2 v-if="activeWindow" class="section-title">
      Registrations — {{ activeWindow.name }}
    </h2>
    <DataTable v-if="activeWindow" :value="registrations" :loading="loadingRegistrations" paginator :rows="15">
      <Column header="Member"><template #body="{ data }">{{ data.user_name }}</template></Column>
      <Column field="status" header="Status" />
      <Column header="Submitted">
        <template #body="{ data }">{{ new Date(data.submitted_at).toLocaleString() }}</template>
      </Column>
      <Column field="notes" header="Notes" />
    </DataTable>

    <Dialog v-model:visible="showCreate" header="New Registration Window" modal style="width:460px">
      <div class="form-field">
        <label>Name</label>
        <InputText v-model="form.name" class="w-full" placeholder="e.g. Catechism 2026 Term 1" />
      </div>
      <div class="form-field">
        <label>Description</label>
        <Textarea v-model="form.description" class="w-full" rows="2" />
      </div>
      <div class="form-row">
        <div class="form-field">
          <label>Opens</label>
          <DatePicker v-model="form.opens_at" showTime hourFormat="12" class="w-full" />
        </div>
        <div class="form-field">
          <label>Closes</label>
          <DatePicker v-model="form.closes_at" showTime hourFormat="12" class="w-full" />
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
import Tag from "primevue/tag";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import DatePicker from "primevue/datepicker";
import { useToast } from "primevue/usetoast";
import registrationService from "../services/registration.service";

const toast = useToast();
const windows = ref([]);
const loadingWindows = ref(true);
const registrations = ref([]);
const loadingRegistrations = ref(false);
const activeWindow = ref(null);
const showCreate = ref(false);
const creating = ref(false);
const form = ref({ name: "", description: "", opens_at: null, closes_at: null });

async function fetchWindows() {
  loadingWindows.value = true;
  try {
    const { data } = await registrationService.listWindows();
    windows.value = data.results || data;
  } finally {
    loadingWindows.value = false;
  }
}

async function viewRegistrations(win) {
  activeWindow.value = win;
  loadingRegistrations.value = true;
  try {
    const { data } = await registrationService.listCatechism({ window: win.id });
    registrations.value = data.results || data;
  } finally {
    loadingRegistrations.value = false;
  }
}

async function submitCreate() {
  creating.value = true;
  try {
    const payload = {
      ...form.value,
      opens_at: form.value.opens_at?.toISOString(),
      closes_at: form.value.closes_at?.toISOString(),
    };
    const { data } = await registrationService.createWindow(payload);
    windows.value.unshift(data);
    showCreate.value = false;
    form.value = { name: "", description: "", opens_at: null, closes_at: null };
    toast.add({ severity: "success", summary: "Registration window created", life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Failed to create", detail: JSON.stringify(e.response?.data), life: 4000 });
  } finally {
    creating.value = false;
  }
}

onMounted(fetchWindows);
</script>

<style scoped>
.section-title { font-size: 1.1rem; font-weight: 600; margin: 0 0 0.75rem; color: #1e293b; }
.header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.mb-4 { margin-bottom: 2rem; }
.form-field { margin-bottom: 1rem; }
.form-field label { display: block; margin-bottom: 0.35rem; font-size: 0.85rem; color: #475569; }
.form-row { display: flex; gap: 1rem; }
.form-row .form-field { flex: 1; }
.w-full { width: 100%; }
</style>
