<template>
  <div>
    <div class="header-row">
      <h2 class="section-title">Bible Versions</h2>
      <Button label="New Version" icon="pi pi-plus" @click="showVersionCreate = true" />
    </div>
    <DataTable :value="versions" :loading="loadingVersions" paginator :rows="10" class="mb-4">
      <Column field="code" header="Code" sortable />
      <Column field="name" header="Name" sortable />
      <Column field="language" header="Language" sortable />
      <Column header="Public Domain">
        <template #body="{ data }">
          <Tag :value="data.is_public_domain ? 'Yes' : 'Copyrighted'" :severity="data.is_public_domain ? 'success' : 'warn'" />
        </template>
      </Column>
    </DataTable>
    <Message severity="info" :closable="false" class="mb-4">
      Verse text is imported separately via <code>manage.py import_bible &lt;file&gt; --code=&lt;VERSION_CODE&gt;</code>
      on the server, once a version exists here. Public-domain translations (e.g. KJV) can be imported freely;
      copyrighted ones (e.g. NIV) require a licensed data source.
    </Message>

    <div class="header-row">
      <h2 class="section-title">Hymns</h2>
      <Button label="New Hymn" icon="pi pi-plus" @click="showHymnCreate = true" />
    </div>
    <DataTable :value="hymns" :loading="loadingHymns" paginator :rows="15" sortMode="multiple">
      <Column field="number" header="No." sortable style="width:80px" />
      <Column field="title" header="Title" sortable />
      <Column field="first_line" header="First Line" />
      <Column header="File">
        <template #body="{ data }">
          <Tag v-if="data.file" :value="data.file.file_type" severity="info" />
          <span v-else style="color:#94a3b8;">No file yet</span>
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="showVersionCreate" header="New Bible Version" modal style="width:420px">
      <div class="form-field">
        <label>Code</label>
        <InputText v-model="versionForm.code" class="w-full" placeholder="e.g. KJV, NIV, SUV" />
      </div>
      <div class="form-field">
        <label>Full Name</label>
        <InputText v-model="versionForm.name" class="w-full" placeholder="e.g. King James Version" />
      </div>
      <div class="form-field">
        <label>Language</label>
        <InputText v-model="versionForm.language" class="w-full" placeholder="e.g. English, Kiswahili" />
      </div>
      <div class="form-field checkbox-row">
        <Checkbox v-model="versionForm.is_public_domain" binary inputId="pd" />
        <label for="pd">Public domain (free to import text)</label>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="showVersionCreate = false" />
        <Button label="Create" :loading="creatingVersion" @click="submitVersion" />
      </template>
    </Dialog>

    <Dialog v-model:visible="showHymnCreate" header="New Hymn" modal style="width:460px">
      <div class="form-row">
        <div class="form-field">
          <label>Number</label>
          <InputNumber v-model="hymnForm.number" class="w-full" />
        </div>
        <div class="form-field" style="flex:2">
          <label>Title</label>
          <InputText v-model="hymnForm.title" class="w-full" />
        </div>
      </div>
      <div class="form-field">
        <label>First Line</label>
        <InputText v-model="hymnForm.first_line" class="w-full" placeholder="For search, e.g. 'Amazing grace how sweet...'" />
      </div>
      <div class="form-field">
        <label>File Type</label>
        <Select v-model="hymnForm.file_type" :options="fileTypeOptions" optionLabel="label" optionValue="value" class="w-full" />
      </div>
      <div v-if="hymnForm.file_type === 'text'" class="form-field">
        <label>Text Content</label>
        <Textarea v-model="hymnForm.text_content" class="w-full" rows="5" />
      </div>
      <div v-else class="form-field">
        <label>Upload File ({{ hymnForm.file_type.toUpperCase() }})</label>
        <FileUpload
          mode="basic"
          :auto="false"
          chooseLabel="Choose File"
          @select="onFileSelect"
          :accept="acceptFor(hymnForm.file_type)"
        />
        <span v-if="selectedFile" class="file-name">{{ selectedFile.name }}</span>
      </div>
      <div class="form-field">
        <label>Branch (uploader's branch, optional)</label>
        <Select v-model="hymnForm.branch" :options="branches" optionLabel="name" optionValue="id" class="w-full" showClear placeholder="Unspecified" />
      </div>
      <template #footer>
        <Button label="Cancel" text @click="showHymnCreate = false" />
        <Button label="Create" :loading="creatingHymn" @click="submitHymn" />
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
import Message from "primevue/message";
import FileUpload from "primevue/fileupload";
import { useToast } from "primevue/usetoast";
import scriptureService from "../services/scripture.service";
import branchesService from "../services/branches.service";

const toast = useToast();
const versions = ref([]);
const hymns = ref([]);
const branches = ref([]);
const loadingVersions = ref(true);
const loadingHymns = ref(true);

const showVersionCreate = ref(false);
const creatingVersion = ref(false);
const versionForm = ref({ code: "", name: "", language: "", is_public_domain: false });

const showHymnCreate = ref(false);
const creatingHymn = ref(false);
const selectedFile = ref(null);
const hymnForm = ref({ number: null, title: "", first_line: "", file_type: "pdf", text_content: "", branch: null });

const fileTypeOptions = [
  { label: "PDF", value: "pdf" },
  { label: "PowerPoint", value: "ppt" },
  { label: "Image", value: "image" },
  { label: "Text", value: "text" },
];

function acceptFor(type) {
  if (type === "pdf") return "application/pdf";
  if (type === "ppt") return ".ppt,.pptx";
  if (type === "image") return "image/*";
  return undefined;
}

function onFileSelect(event) {
  selectedFile.value = event.files[0];
}

async function fetchVersions() {
  loadingVersions.value = true;
  try {
    const { data } = await scriptureService.listVersions();
    versions.value = data.results || data;
  } finally {
    loadingVersions.value = false;
  }
}

async function fetchHymns() {
  loadingHymns.value = true;
  try {
    const { data } = await scriptureService.listHymns();
    hymns.value = data.results || data;
  } finally {
    loadingHymns.value = false;
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

async function submitVersion() {
  creatingVersion.value = true;
  try {
    const { data } = await scriptureService.createVersion(versionForm.value);
    versions.value.unshift(data);
    showVersionCreate.value = false;
    versionForm.value = { code: "", name: "", language: "", is_public_domain: false };
    toast.add({ severity: "success", summary: "Bible version created", life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Failed to create", detail: JSON.stringify(e.response?.data), life: 4000 });
  } finally {
    creatingVersion.value = false;
  }
}

async function submitHymn() {
  creatingHymn.value = true;
  try {
    const { data: hymn } = await scriptureService.createHymn({
      number: hymnForm.value.number,
      title: hymnForm.value.title,
      first_line: hymnForm.value.first_line,
    });

    const fd = new FormData();
    fd.append("hymn", hymn.id);
    fd.append("file_type", hymnForm.value.file_type);
    if (hymnForm.value.branch) fd.append("branch", hymnForm.value.branch);
    if (hymnForm.value.file_type === "text") {
      fd.append("text_content", hymnForm.value.text_content);
    } else if (selectedFile.value) {
      fd.append("file", selectedFile.value);
    }
    const { data: file } = await scriptureService.createHymnFile(fd);

    hymns.value.unshift({ ...hymn, file });
    showHymnCreate.value = false;
    selectedFile.value = null;
    hymnForm.value = { number: null, title: "", first_line: "", file_type: "pdf", text_content: "", branch: null };
    toast.add({ severity: "success", summary: "Hymn created", life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Failed to create hymn", detail: JSON.stringify(e.response?.data), life: 4000 });
  } finally {
    creatingHymn.value = false;
  }
}

onMounted(() => {
  fetchVersions();
  fetchHymns();
  fetchBranches();
});
</script>

<style scoped>
.section-title { font-size: 1.1rem; font-weight: 600; margin: 0; color: #1e293b; }
.header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.mb-4 { margin-bottom: 2rem; }
.form-field { margin-bottom: 1rem; }
.form-field label { display: block; margin-bottom: 0.35rem; font-size: 0.85rem; color: #475569; }
.form-row { display: flex; gap: 1rem; }
.checkbox-row { display: flex; align-items: center; gap: 0.5rem; }
.checkbox-row label { margin: 0; }
.file-name { display: block; margin-top: 0.5rem; font-size: 0.85rem; color: #475569; }
.w-full { width: 100%; }
</style>
