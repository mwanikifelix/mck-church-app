<template>
  <div>
    <div class="header-row">
      <h2 class="section-title">Growth-Track Groups</h2>
      <Button label="New Group" icon="pi pi-plus" @click="showCreate = true" />
    </div>
    <DataTable :value="store.items" :loading="store.loading" paginator :rows="15">
      <Column field="name" header="Name" sortable />
      <Column field="branch" header="Branch" />
      <Column header="Age Range">
        <template #body="{ data }">{{ data.min_age }} - {{ data.max_age }}</template>
      </Column>
      <Column header="Active">
        <template #body="{ data }">
          <Tag :value="data.is_active ? 'Yes' : 'No'" :severity="data.is_active ? 'success' : 'secondary'" />
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="showCreate" header="New Growth-Track Group" modal style="width:460px">
      <div class="form-field">
        <label>Name</label>
        <InputText v-model="form.name" class="w-full" placeholder="e.g. Youth - Wesley Mombasa" />
      </div>
      <div class="form-field">
        <label>Branch</label>
        <Select v-model="form.branch" :options="branches" optionLabel="name" optionValue="id" class="w-full" placeholder="Select branch" />
      </div>
      <div class="form-field">
        <label>Description</label>
        <Textarea v-model="form.description" class="w-full" rows="2" />
      </div>
      <div class="form-row">
        <div class="form-field">
          <label>Min Age</label>
          <InputNumber v-model="form.min_age" class="w-full" />
        </div>
        <div class="form-field">
          <label>Max Age</label>
          <InputNumber v-model="form.max_age" class="w-full" />
        </div>
      </div>
      <div class="form-field">
        <label>Marital Status Requirement</label>
        <Select v-model="form.marital_status_requirement" :options="maritalOptions" optionLabel="label" optionValue="value" class="w-full" />
      </div>
      <div class="form-field checkbox-row">
        <Checkbox v-model="form.enforce_eligibility" binary inputId="enforce" />
        <label for="enforce">Enforce age/marital eligibility on join</label>
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
import InputNumber from "primevue/inputnumber";
import Textarea from "primevue/textarea";
import Select from "primevue/select";
import Checkbox from "primevue/checkbox";
import { useToast } from "primevue/usetoast";
import { useGroupsStore } from "../store/groups";
import groupsService from "../services/groups.service";
import branchesService from "../services/branches.service";

const store = useGroupsStore();
const toast = useToast();
const branches = ref([]);
const showCreate = ref(false);
const creating = ref(false);
const maritalOptions = [
  { label: "Any", value: "any" },
  { label: "Single only", value: "single" },
  { label: "Married only", value: "married" },
];
const form = ref({
  name: "", branch: null, description: "", min_age: 0, max_age: 120,
  marital_status_requirement: "any", enforce_eligibility: false,
});

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
    const { data } = await groupsService.create(form.value);
    store.items.unshift(data);
    showCreate.value = false;
    form.value = {
      name: "", branch: null, description: "", min_age: 0, max_age: 120,
      marital_status_requirement: "any", enforce_eligibility: false,
    };
    toast.add({ severity: "success", summary: "Group created", life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Failed to create", detail: JSON.stringify(e.response?.data), life: 4000 });
  } finally {
    creating.value = false;
  }
}

onMounted(() => {
  store.fetchAll();
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
.checkbox-row { display: flex; align-items: center; gap: 0.5rem; }
.checkbox-row label { margin: 0; }
.w-full { width: 100%; }
</style>
