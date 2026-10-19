<template>
  <div>
    <BasePageHeading
      title="Content Library"
      icon="fa-book-open"
      subtitle="Bible versions and hymns available in the church app"
    />

    <div class="content">
    <!-- Bible versions -->
    <div class="header-row mb-3">
      <div>
        <h3 class="section-title mb-0">Bible Versions</h3>
        <p class="text-muted fs-sm mb-0">
          {{ versions.length }} {{ versions.length === 1 ? "version" : "versions" }}
        </p>
      </div>
      <button type="button" class="btn btn-primary btn-sm" @click="openVersionCreate">
        <i class="fa fa-plus me-1"></i> New Version
      </button>
    </div>

    <AppDataTable
      :rows="versions"
      :columns="versionColumns"
      :loading="loadingVersions"
      :page-size="10"
      :search-fields="['code', 'name', 'language']"
      search-placeholder="Search code, name or language…"
      export-name="bible-versions"
      empty-text="No Bible versions yet. Create the first one."
      empty-icon="fa-book"
    >
      <template #public-domain="{ row }">
        <span
          class="badge rounded-pill"
          :class="
            row.is_public_domain
              ? 'bg-success-subtle text-success-emphasis'
              : 'bg-warning-subtle text-warning-emphasis'
          "
        >
          {{ row.is_public_domain ? "Yes" : "Copyrighted" }}
        </span>
      </template>
    </AppDataTable>

    <div class="alert alert-info d-flex align-items-start gap-2 mb-4" role="alert">
      <i class="fa fa-info-circle mt-1"></i>
      <div>
        Verse text is imported separately via
        <code>manage.py import_bible &lt;file&gt; --code=&lt;VERSION_CODE&gt;</code> on the server,
        once a version exists here. Public-domain translations (e.g. KJV) can be imported freely;
        copyrighted ones (e.g. NIV) require a licensed data source.
      </div>
    </div>

    <!-- Hymns -->
    <div class="header-row mb-3">
      <div>
        <h3 class="section-title mb-0">Hymns</h3>
        <p class="text-muted fs-sm mb-0">{{ hymns.length }} hymns</p>
      </div>
      <button type="button" class="btn btn-primary btn-sm" @click="openHymnCreate">
        <i class="fa fa-plus me-1"></i> New Hymn
      </button>
    </div>

    <AppDataTable
      :rows="hymns"
      :columns="hymnColumns"
      :loading="loadingHymns"
      :page-size="15"
      search-placeholder="Search number, title or first line…"
      export-name="hymns"
      empty-text="No hymns yet. Create the first one."
      empty-icon="fa-music"
    >
      <template #file="{ row }">
        <span v-if="row.file" class="badge rounded-pill bg-info-subtle text-info-emphasis">
          {{ row.file.file_type }}
        </span>
        <span v-else class="text-muted">No file yet</span>
      </template>
    </AppDataTable>

    <!-- New Bible version dialog -->
    <AppModal
      v-model:visible="showVersionCreate"
      title="New Bible Version"
      subtitle="Add a translation for verse lookups"
      size="sm"
    >
      <FormField
        label="Code"
        required
        :error="versionErrors.code"
        field-id="cl-v-code"
        hint="Short abbreviation shown in the reader"
      >
        <input
          id="cl-v-code"
          v-model="versionForm.code"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': versionErrors.code }"
          placeholder="e.g. KJV, NIV, SUV"
        />
      </FormField>

      <FormField label="Full Name" required :error="versionErrors.name" field-id="cl-v-name">
        <input
          id="cl-v-name"
          v-model="versionForm.name"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': versionErrors.name }"
          placeholder="e.g. King James Version"
        />
      </FormField>

      <FormField label="Language" required :error="versionErrors.language" field-id="cl-v-lang">
        <input
          id="cl-v-lang"
          v-model="versionForm.language"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': versionErrors.language }"
          placeholder="e.g. English, Kiswahili"
        />
      </FormField>

      <div class="form-check mb-1">
        <input
          id="cl-v-pd"
          v-model="versionForm.is_public_domain"
          type="checkbox"
          class="form-check-input"
        />
        <label class="form-check-label" for="cl-v-pd">Public domain (free to import text)</label>
      </div>

      <template #footer>
        <button type="button" class="btn btn-alt-secondary btn-sm" @click="showVersionCreate = false">
          Cancel
        </button>
        <button
          type="button"
          class="btn btn-primary btn-sm"
          :disabled="creatingVersion"
          @click="submitVersion"
        >
          <span v-if="creatingVersion" class="spinner-border spinner-border-sm me-1"></span>
          Create version
        </button>
      </template>
    </AppModal>

    <!-- New hymn dialog -->
    <AppModal
      v-model:visible="showHymnCreate"
      title="New Hymn"
      subtitle="Register a hymn and attach its sheet or text"
    >
      <div class="row g-3">
        <div class="col-12 col-sm-4">
          <FormField label="Number" required :error="hymnErrors.number" field-id="cl-h-number">
            <input
              id="cl-h-number"
              v-model.number="hymnForm.number"
              type="number"
              min="1"
              class="form-control"
              :class="{ 'is-invalid': hymnErrors.number }"
            />
          </FormField>
        </div>
        <div class="col-12 col-sm-8">
          <FormField label="Title" required :error="hymnErrors.title" field-id="cl-h-title">
            <input
              id="cl-h-title"
              v-model="hymnForm.title"
              type="text"
              class="form-control"
              :class="{ 'is-invalid': hymnErrors.title }"
            />
          </FormField>
        </div>
      </div>

      <FormField
        label="First Line"
        :error="hymnErrors.first_line"
        field-id="cl-h-first"
        hint="Used for search as members type"
      >
        <input
          id="cl-h-first"
          v-model="hymnForm.first_line"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': hymnErrors.first_line }"
          placeholder="e.g. 'Amazing grace how sweet...'"
        />
      </FormField>

      <FormField label="File Type" required field-id="cl-h-type">
        <select id="cl-h-type" v-model="hymnForm.file_type" class="form-select">
          <option v-for="opt in fileTypeOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
      </FormField>

      <FormField
        v-if="hymnForm.file_type === 'text'"
        label="Text Content"
        required
        :error="hymnErrors.text_content"
        field-id="cl-h-text"
      >
        <textarea
          id="cl-h-text"
          v-model="hymnForm.text_content"
          rows="5"
          class="form-control"
          :class="{ 'is-invalid': hymnErrors.text_content }"
        ></textarea>
      </FormField>
      <FormField
        v-else
        :label="`Upload File (${hymnForm.file_type.toUpperCase()})`"
        required
        :error="hymnErrors.file"
        field-id="cl-h-file"
        hint="Attach the sheet or lyric file"
      >
        <input
          id="cl-h-file"
          type="file"
          class="form-control"
          :class="{ 'is-invalid': hymnErrors.file }"
          :accept="acceptFor(hymnForm.file_type)"
          @change="onFileChange"
        />
        <div v-if="selectedFile" class="fs-sm text-muted mt-1">
          <i class="fa fa-file me-1"></i>{{ selectedFile.name }}
        </div>
      </FormField>

      <FormField
        label="Branch"
        :error="hymnErrors.branch"
        field-id="cl-h-branch"
        hint="Uploader's branch, optional"
      >
        <select id="cl-h-branch" v-model="hymnForm.branch" class="form-select">
          <option :value="null">Unspecified</option>
          <option v-for="b in branches" :key="b.id" :value="b.id">{{ b.name }}</option>
        </select>
      </FormField>

      <template #footer>
        <button type="button" class="btn btn-alt-secondary btn-sm" @click="showHymnCreate = false">
          Cancel
        </button>
        <button
          type="button"
          class="btn btn-primary btn-sm"
          :disabled="creatingHymn"
          @click="submitHymn"
        >
          <span v-if="creatingHymn" class="spinner-border spinner-border-sm me-1"></span>
          Create hymn
        </button>
      </template>
    </AppModal>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "../composables/useToast";
import scriptureService from "../services/scripture.service";
import branchesService from "../services/branches.service";

const toast = useToast();
const versions = ref([]);
const hymns = ref([]);
const branches = ref([]);
const loadingVersions = ref(true);
const loadingHymns = ref(true);

const versionColumns = [
  { field: "code", header: "Code", sortable: true, strong: true },
  { field: "name", header: "Name", sortable: true },
  { field: "language", header: "Language", sortable: true },
  { header: "Public Domain", slot: "public-domain" },
];

const hymnColumns = [
  { field: "number", header: "No.", sortable: true, width: "80px" },
  { field: "title", header: "Title", sortable: true, strong: true },
  { field: "first_line", header: "First Line" },
  { header: "File", slot: "file" },
];

const showVersionCreate = ref(false);
const creatingVersion = ref(false);
const versionForm = ref({ code: "", name: "", language: "", is_public_domain: false });
const versionErrors = ref({});

const showHymnCreate = ref(false);
const creatingHymn = ref(false);
const selectedFile = ref(null);
const hymnForm = ref({
  number: null,
  title: "",
  first_line: "",
  file_type: "pdf",
  text_content: "",
  branch: null,
});
const hymnErrors = ref({});

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

function onFileChange(event) {
  selectedFile.value = event.target.files?.[0] || null;
}

/** Turn a Django error body ({ field: [msgs] }) into { field: message }. */
function apiErrorMessages(e) {
  const api = e.response?.data;
  const mapped = {};
  if (api && typeof api === "object") {
    Object.entries(api).forEach(([k, v]) => {
      mapped[k] = Array.isArray(v) ? v.join(" ") : String(v);
    });
  }
  return mapped;
}

function openVersionCreate() {
  versionForm.value = { code: "", name: "", language: "", is_public_domain: false };
  versionErrors.value = {};
  showVersionCreate.value = true;
}

function validateVersion() {
  const e = {};
  const f = versionForm.value;
  if (!String(f.code || "").trim()) e.code = "Code is required.";
  if (!String(f.name || "").trim()) e.name = "Full name is required.";
  if (!String(f.language || "").trim()) e.language = "Language is required.";
  versionErrors.value = e;
  return Object.keys(e).length === 0;
}

function openHymnCreate() {
  hymnForm.value = {
    number: null,
    title: "",
    first_line: "",
    file_type: "pdf",
    text_content: "",
    branch: null,
  };
  selectedFile.value = null;
  hymnErrors.value = {};
  showHymnCreate.value = true;
}

function validateHymn() {
  const e = {};
  const f = hymnForm.value;
  if (f.number === null || f.number === "" || Number.isNaN(Number(f.number)))
    e.number = "Number is required.";
  else if (Number(f.number) < 1) e.number = "Number must be 1 or greater.";
  if (!String(f.title || "").trim()) e.title = "Title is required.";
  if (f.file_type === "text") {
    if (!String(f.text_content || "").trim()) e.text_content = "Paste the hymn text.";
  } else if (!selectedFile.value) {
    e.file = "Choose a file to upload.";
  }
  hymnErrors.value = e;
  return Object.keys(e).length === 0;
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
  if (!validateVersion()) return;

  creatingVersion.value = true;
  try {
    const { data } = await scriptureService.createVersion(versionForm.value);
    versions.value.unshift(data);
    showVersionCreate.value = false;
    versionForm.value = { code: "", name: "", language: "", is_public_domain: false };
    versionErrors.value = {};
    toast.add({ severity: "success", summary: "Bible version created", life: 2500 });
  } catch (e) {
    const mapped = apiErrorMessages(e);
    versionErrors.value = { ...versionErrors.value, ...mapped };
    toast.add({
      severity: "error",
      summary: "Failed to create",
      detail: Object.values(mapped)[0] || e.message,
      life: 5000,
    });
  } finally {
    creatingVersion.value = false;
  }
}

async function submitHymn() {
  if (!validateHymn()) return;

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
    hymnForm.value = {
      number: null,
      title: "",
      first_line: "",
      file_type: "pdf",
      text_content: "",
      branch: null,
    };
    hymnErrors.value = {};
    toast.add({ severity: "success", summary: "Hymn created", life: 2500 });
  } catch (e) {
    const mapped = apiErrorMessages(e);
    hymnErrors.value = { ...hymnErrors.value, ...mapped };
    toast.add({
      severity: "error",
      summary: "Failed to create hymn",
      detail: Object.values(mapped)[0] || e.message,
      life: 5000,
    });
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
