<template>
  <div>
    <div class="header-row">
      <h2 class="section-title">Events</h2>
      <Button label="New Event" icon="pi pi-plus" @click="showCreate = true" />
    </div>
    <DataTable :value="events" :loading="loading" paginator :rows="15" sortMode="multiple">
      <Column field="title" header="Title" sortable />
      <Column header="Start" sortable sortField="start_time">
        <template #body="{ data }">{{ new Date(data.start_time).toLocaleString() }}</template>
      </Column>
      <Column field="location" header="Location" />
      <Column field="rsvp_count" header="RSVPs" sortable />
    </DataTable>

    <Dialog v-model:visible="showCreate" header="New Event" modal style="width:460px">
      <div class="form-field">
        <label>Title</label>
        <InputText v-model="form.title" class="w-full" />
      </div>
      <div class="form-field">
        <label>Description</label>
        <Textarea v-model="form.description" class="w-full" rows="2" />
      </div>
      <div class="form-field">
        <label>Location</label>
        <InputText v-model="form.location" class="w-full" />
      </div>
      <div class="form-row">
        <div class="form-field">
          <label>Start Time</label>
          <DatePicker v-model="form.start_time" showTime hourFormat="12" class="w-full" />
        </div>
        <div class="form-field">
          <label>End Time</label>
          <DatePicker v-model="form.end_time" showTime hourFormat="12" class="w-full" />
        </div>
      </div>
      <div class="form-field">
        <label>Branch (leave blank for church-wide)</label>
        <Select v-model="form.branch" :options="branches" optionLabel="name" optionValue="id" class="w-full" showClear placeholder="Church-wide" />
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
import DatePicker from "primevue/datepicker";
import Select from "primevue/select";
import { useToast } from "primevue/usetoast";
import eventsService from "../services/events.service";
import branchesService from "../services/branches.service";

const toast = useToast();
const events = ref([]);
const branches = ref([]);
const loading = ref(true);
const showCreate = ref(false);
const creating = ref(false);
const form = ref({ title: "", description: "", location: "", start_time: null, end_time: null, branch: null });

async function fetchEvents() {
  loading.value = true;
  try {
    const { data } = await eventsService.list();
    events.value = data.results || data;
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
    const payload = {
      ...form.value,
      start_time: form.value.start_time?.toISOString(),
      end_time: form.value.end_time?.toISOString() || null,
    };
    const { data } = await eventsService.create(payload);
    events.value.unshift(data);
    showCreate.value = false;
    form.value = { title: "", description: "", location: "", start_time: null, end_time: null, branch: null };
    toast.add({ severity: "success", summary: "Event created", life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Failed to create", detail: JSON.stringify(e.response?.data), life: 4000 });
  } finally {
    creating.value = false;
  }
}

onMounted(() => {
  fetchEvents();
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
