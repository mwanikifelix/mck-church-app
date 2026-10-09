<template>
  <div>
    <div class="header-row">
      <h2 class="section-title">Announcements</h2>
      <Button label="New Announcement" icon="pi pi-plus" @click="showCreate = true" />
    </div>
    <DataTable :value="announcements" :loading="loading" paginator :rows="15">
      <Column field="title" header="Title" sortable />
      <Column field="body" header="Body" />
      <Column header="Pinned">
        <template #body="{ data }">
          <Tag v-if="data.is_pinned" value="Pinned" severity="warn" />
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="showCreate" header="New Announcement" modal style="width:420px">
      <div class="form-field">
        <label>Title</label>
        <InputText v-model="form.title" class="w-full" />
      </div>
      <div class="form-field">
        <label>Body</label>
        <Textarea v-model="form.body" class="w-full" rows="4" />
      </div>
      <div class="form-field">
        <label>Branch (leave blank for church-wide)</label>
        <Select v-model="form.branch" :options="branches" optionLabel="name" optionValue="id" class="w-full" showClear placeholder="Church-wide" />
      </div>
      <div class="form-field checkbox-row">
        <Checkbox v-model="form.is_pinned" binary inputId="pinned" />
        <label for="pinned">Pin to top</label>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="showCreate = false" />
        <Button label="Publish" :loading="creating" @click="submitCreate" />
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
import Select from "primevue/select";
import Checkbox from "primevue/checkbox";
import { useToast } from "primevue/usetoast";
import contentService from "../services/content.service";
import branchesService from "../services/branches.service";

const toast = useToast();
const announcements = ref([]);
const branches = ref([]);
const loading = ref(true);
const showCreate = ref(false);
const creating = ref(false);
const form = ref({ title: "", body: "", branch: null, is_pinned: false });

async function fetchAnnouncements() {
  loading.value = true;
  try {
    const { data } = await contentService.listAnnouncements();
    announcements.value = data.results || data;
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
    const { data } = await contentService.createAnnouncement(form.value);
    announcements.value.unshift(data);
    showCreate.value = false;
    form.value = { title: "", body: "", branch: null, is_pinned: false };
    toast.add({ severity: "success", summary: "Announcement published", life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Failed to publish", detail: JSON.stringify(e.response?.data), life: 4000 });
  } finally {
    creating.value = false;
  }
}

onMounted(() => {
  fetchAnnouncements();
  fetchBranches();
});
</script>

<style scoped>
.section-title { font-size: 1.1rem; font-weight: 600; margin: 0; color: #1e293b; }
.header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.form-field { margin-bottom: 1rem; }
.form-field label { display: block; margin-bottom: 0.35rem; font-size: 0.85rem; color: #475569; }
.checkbox-row { display: flex; align-items: center; gap: 0.5rem; }
.checkbox-row label { margin: 0; }
.w-full { width: 100%; }
</style>
