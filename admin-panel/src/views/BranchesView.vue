<template>
  <div>
    <div class="header-row">
      <h2 class="section-title">Branches</h2>
      <Button label="New Branch" icon="pi pi-plus" @click="showCreate = true" />
    </div>
    <DataTable :value="branches" :loading="loading" paginator :rows="15">
      <Column field="name" header="Name" sortable />
      <Column field="short_description" header="Description" />
      <Column field="address" header="Address" />
      <Column field="attendance_radius_meters" header="Check-in Radius (m)" />
    </DataTable>

    <Dialog v-model:visible="showCreate" header="New Branch" modal style="width:460px">
      <div class="form-field">
        <label>Name</label>
        <InputText v-model="form.name" class="w-full" placeholder="e.g. MCK Voi Church" />
      </div>
      <div class="form-field">
        <label>Short Description</label>
        <InputText v-model="form.short_description" class="w-full" placeholder="e.g. Located near Samburu Primary School" />
      </div>
      <div class="form-field">
        <label>Address</label>
        <InputText v-model="form.address" class="w-full" />
      </div>
      <div class="form-row">
        <div class="form-field">
          <label>Latitude</label>
          <InputNumber v-model="form.latitude" class="w-full" :minFractionDigits="6" :maxFractionDigits="6" />
        </div>
        <div class="form-field">
          <label>Longitude</label>
          <InputNumber v-model="form.longitude" class="w-full" :minFractionDigits="6" :maxFractionDigits="6" />
        </div>
      </div>
      <div class="form-field">
        <label>Attendance Check-in Radius (meters)</label>
        <InputNumber v-model="form.attendance_radius_meters" class="w-full" />
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
import { useToast } from "primevue/usetoast";
import branchesService from "../services/branches.service";

const toast = useToast();
const branches = ref([]);
const loading = ref(true);
const showCreate = ref(false);
const creating = ref(false);
const form = ref({
  name: "", short_description: "", address: "",
  latitude: null, longitude: null, attendance_radius_meters: 100,
});

async function fetchBranches() {
  loading.value = true;
  try {
    const { data } = await branchesService.list();
    branches.value = data.results || data;
  } finally {
    loading.value = false;
  }
}

async function submitCreate() {
  creating.value = true;
  try {
    const { data } = await branchesService.create(form.value);
    branches.value.unshift(data);
    showCreate.value = false;
    form.value = {
      name: "", short_description: "", address: "",
      latitude: null, longitude: null, attendance_radius_meters: 100,
    };
    toast.add({ severity: "success", summary: "Branch created", life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Failed to create", detail: JSON.stringify(e.response?.data), life: 4000 });
  } finally {
    creating.value = false;
  }
}

onMounted(fetchBranches);
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
