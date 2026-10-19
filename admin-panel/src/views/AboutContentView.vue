<template>
  <div>
    <BasePageHeading
      title="About Page Content"
      icon="fa-info-circle"
      subtitle="What visitors see on the public church website"
    />

    <div class="content">
    <!-- Tabs -->
    <ul class="nav nav-tabs mb-3" role="tablist">
      <li class="nav-item" role="presentation">
        <button
          type="button"
          class="nav-link"
          :class="{ active: tab === 'profile' }"
          @click="tab = 'profile'"
        >
          Church Profile
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button
          type="button"
          class="nav-link"
          :class="{ active: tab === 'gallery' }"
          @click="tab = 'gallery'"
        >
          Gallery
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button
          type="button"
          class="nav-link"
          :class="{ active: tab === 'facilities' }"
          @click="tab = 'facilities'"
        >
          Facilities
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button
          type="button"
          class="nav-link"
          :class="{ active: tab === 'schedule' }"
          @click="tab = 'schedule'"
        >
          Service Schedule
        </button>
      </li>
    </ul>

    <div class="tab-content">
      <!-- Church profile -->
      <div v-show="tab === 'profile'" class="tab-pane fade show active" role="tabpanel">
        <div v-if="loadingProfile" class="text-center py-5">
          <span class="spinner-border spinner-border-sm" role="status"></span>
        </div>

        <div v-else class="panel-body" style="max-width: 600px">
          <FormField
            label="Church Name"
            required
            :error="profileErrors.name"
            field-id="ac-name"
          >
            <input
              id="ac-name"
              v-model="profile.name"
              type="text"
              class="form-control"
              :class="{ 'is-invalid': profileErrors.name }"
            />
          </FormField>

          <FormField
            label="Tagline"
            :error="profileErrors.tagline"
            field-id="ac-tagline"
            hint="Shown under the church name"
          >
            <input
              id="ac-tagline"
              v-model="profile.tagline"
              type="text"
              class="form-control"
              :class="{ 'is-invalid': profileErrors.tagline }"
              placeholder="e.g. Witnessing for Christ in Transforming lives"
            />
          </FormField>

          <div class="row g-3">
            <div class="col-12 col-sm-6">
              <FormField label="Theme of the Year" field-id="ac-theme">
                <input
                  id="ac-theme"
                  v-model="profile.theme_title"
                  type="text"
                  class="form-control"
                />
              </FormField>
            </div>
            <div class="col-12 col-sm-6">
              <FormField label="Scripture Reference" field-id="ac-theme-ref">
                <input
                  id="ac-theme-ref"
                  v-model="profile.theme_scripture_reference"
                  type="text"
                  class="form-control"
                  placeholder="e.g. Genesis 8:1a"
                />
              </FormField>
            </div>
          </div>

          <FormField label="Theme Scripture Text" field-id="ac-theme-text">
            <textarea
              id="ac-theme-text"
              v-model="profile.theme_scripture_text"
              rows="2"
              class="form-control"
            ></textarea>
          </FormField>

          <FormField label="Mission" field-id="ac-mission">
            <textarea
              id="ac-mission"
              v-model="profile.mission"
              rows="2"
              class="form-control"
            ></textarea>
          </FormField>

          <FormField label="Vision" field-id="ac-vision">
            <textarea
              id="ac-vision"
              v-model="profile.vision"
              rows="2"
              class="form-control"
            ></textarea>
          </FormField>

          <FormField label="Motto" field-id="ac-motto">
            <input id="ac-motto" v-model="profile.motto" type="text" class="form-control" />
          </FormField>

          <div class="row g-3">
            <div class="col-12 col-sm-6">
              <FormField label="Email" :error="profileErrors.email" field-id="ac-email">
                <input
                  id="ac-email"
                  v-model="profile.email"
                  type="email"
                  class="form-control"
                  :class="{ 'is-invalid': profileErrors.email }"
                />
              </FormField>
            </div>
            <div class="col-12 col-sm-6">
              <FormField label="Location" field-id="ac-location">
                <input
                  id="ac-location"
                  v-model="profile.location"
                  type="text"
                  class="form-control"
                />
              </FormField>
            </div>
          </div>

          <button
            v-if="$can('membership.manage_status')"
            type="button"
            class="btn btn-primary btn-sm"
            :disabled="savingProfile"
            @click="saveProfile"
          >
            <span v-if="savingProfile" class="spinner-border spinner-border-sm me-1"></span>
            <i v-else class="fa fa-save me-1"></i>
            Save Church Profile
          </button>
        </div>
      </div>

      <!-- Gallery -->
      <div v-show="tab === 'gallery'" class="tab-pane fade show active" role="tabpanel">
        <div class="header-row mb-3">
          <div>
            <h3 class="section-title mb-0">Gallery</h3>
            <p class="text-muted fs-sm mb-0">{{ gallery.length }} photos</p>
          </div>
          <button
            v-if="$can('ict.manage_content')"
            type="button"
            class="btn btn-primary btn-sm"
            @click="openPhotoUpload"
          >
            <i class="fa fa-upload me-1"></i> Upload Photo
          </button>
        </div>

        <div v-if="gallery.length" class="gallery-grid">
          <div v-for="photo in gallery" :key="photo.id" class="gallery-item">
            <img :src="photo.image" :alt="photo.caption" />
            <div class="gallery-caption">{{ photo.caption }}</div>
          </div>
        </div>
        <p v-else class="text-muted mb-0">No photos yet. Upload the first one.</p>
      </div>

      <!-- Facilities -->
      <div v-show="tab === 'facilities'" class="tab-pane fade show active" role="tabpanel">
        <div class="header-row mb-3">
          <div>
            <h3 class="section-title mb-0">Facilities</h3>
            <p class="text-muted fs-sm mb-0">{{ facilities.length }} listed</p>
          </div>
          <button
            v-if="$can('content.manage')"
            type="button"
            class="btn btn-primary btn-sm"
            @click="openFacilityCreate"
          >
            <i class="fa fa-plus me-1"></i> New Facility
          </button>
        </div>

        <AppDataTable
          :rows="facilities"
          :columns="facilityColumns"
          :loading="loadingFacilities"
          :page-size="10"
          search-placeholder="Search facilities…"
          export-name="facilities"
          empty-text="No facilities yet."
          empty-icon="fa-building"
        />
      </div>

      <!-- Service schedule -->
      <div v-show="tab === 'schedule'" class="tab-pane fade show active" role="tabpanel">
        <div class="header-row mb-3">
          <div>
            <h3 class="section-title mb-0">Service Schedule</h3>
            <p class="text-muted fs-sm mb-0">{{ schedule.length }} rows</p>
          </div>
          <button
            v-if="$can('content.manage')"
            type="button"
            class="btn btn-primary btn-sm"
            @click="openScheduleCreate"
          >
            <i class="fa fa-plus me-1"></i> Add Row
          </button>
        </div>

        <AppDataTable
          :rows="schedule"
          :columns="scheduleColumns"
          :loading="loadingSchedule"
          :page-size="15"
          search-placeholder="Search services…"
          export-name="service-schedule"
          empty-text="No services scheduled yet."
          empty-icon="fa-clock"
        />
      </div>
    </div>

    <!-- Upload gallery photo dialog -->
    <AppModal
      v-model:visible="showPhotoUpload"
      title="Upload Gallery Photo"
      subtitle="Appears in the public gallery"
      size="sm"
    >
      <FormField label="Image" required :error="photoErrors.image" field-id="ac-photo">
        <input
          id="ac-photo"
          type="file"
          class="form-control"
          :class="{ 'is-invalid': photoErrors.image }"
          accept="image/*"
          @change="onPhotoChange"
        />
        <div v-if="selectedPhoto" class="fs-sm text-muted mt-1">
          <i class="fa fa-image me-1"></i>{{ selectedPhoto.name }}
        </div>
      </FormField>

      <FormField
        label="Caption"
        :error="photoErrors.caption"
        field-id="ac-caption"
        hint="Shown under the photo"
      >
        <input
          id="ac-caption"
          v-model="photoForm.caption"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': photoErrors.caption }"
          placeholder="e.g. Easter Sunday service"
        />
      </FormField>

      <FormField
        label="Branch"
        :error="photoErrors.branch"
        field-id="ac-photo-branch"
        hint="Leave blank for church-wide"
      >
        <select id="ac-photo-branch" v-model="photoForm.branch" class="form-select">
          <option :value="null">Church-wide</option>
          <option v-for="b in branches" :key="b.id" :value="b.id">{{ b.name }}</option>
        </select>
      </FormField>

      <template #footer>
        <button type="button" class="btn btn-alt-secondary btn-sm" @click="showPhotoUpload = false">
          Cancel
        </button>
        <button
          type="button"
          class="btn btn-primary btn-sm"
          :disabled="uploadingPhoto"
          @click="submitPhoto"
        >
          <span v-if="uploadingPhoto" class="spinner-border spinner-border-sm me-1"></span>
          <i v-else class="fa fa-upload me-1"></i>
          Upload
        </button>
      </template>
    </AppModal>

    <!-- New facility dialog -->
    <AppModal
      v-model:visible="showFacilityCreate"
      title="New Facility"
      subtitle="A space shown on the About page"
      size="sm"
    >
      <FormField
        label="Name"
        required
        :error="facilityErrors.name"
        field-id="ac-fac-name"
      >
        <input
          id="ac-fac-name"
          v-model="facilityForm.name"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': facilityErrors.name }"
          placeholder="e.g. Multi Purpose Hall"
        />
      </FormField>

      <FormField
        label="Description"
        :error="facilityErrors.description"
        field-id="ac-fac-desc"
        hint="What the space is used for"
      >
        <textarea
          id="ac-fac-desc"
          v-model="facilityForm.description"
          rows="3"
          class="form-control"
          :class="{ 'is-invalid': facilityErrors.description }"
        ></textarea>
      </FormField>

      <FormField
        label="Branch"
        :error="facilityErrors.branch"
        field-id="ac-fac-branch"
        hint="Leave blank for church-wide"
      >
        <select id="ac-fac-branch" v-model="facilityForm.branch" class="form-select">
          <option :value="null">Church-wide</option>
          <option v-for="b in branches" :key="b.id" :value="b.id">{{ b.name }}</option>
        </select>
      </FormField>

      <template #footer>
        <button
          type="button"
          class="btn btn-alt-secondary btn-sm"
          @click="showFacilityCreate = false"
        >
          Cancel
        </button>
        <button
          type="button"
          class="btn btn-primary btn-sm"
          :disabled="creatingFacility"
          @click="submitFacility"
        >
          <span v-if="creatingFacility" class="spinner-border spinner-border-sm me-1"></span>
          Create facility
        </button>
      </template>
    </AppModal>

    <!-- New schedule row dialog -->
    <AppModal
      v-model:visible="showScheduleCreate"
      title="New Schedule Row"
      subtitle="A service shown in the public schedule"
      size="sm"
    >
      <FormField
        label="Service Name"
        required
        :error="scheduleErrors.name"
        field-id="ac-sch-name"
      >
        <input
          id="ac-sch-name"
          v-model="scheduleForm.name"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': scheduleErrors.name }"
          placeholder="e.g. 1st Service"
        />
      </FormField>

      <div class="row g-3">
        <div class="col-12 col-sm-6">
          <FormField label="Day" required :error="scheduleErrors.day" field-id="ac-sch-day">
            <input
              id="ac-sch-day"
              v-model="scheduleForm.day"
              type="text"
              class="form-control"
              :class="{ 'is-invalid': scheduleErrors.day }"
              placeholder="e.g. Sunday"
            />
          </FormField>
        </div>
        <div class="col-12 col-sm-6">
          <FormField label="Time" required :error="scheduleErrors.time" field-id="ac-sch-time">
            <input
              id="ac-sch-time"
              v-model="scheduleForm.time"
              type="text"
              class="form-control"
              :class="{ 'is-invalid': scheduleErrors.time }"
              placeholder="e.g. 8:00AM"
            />
          </FormField>
        </div>
      </div>

      <FormField label="Order" required :error="scheduleErrors.order" field-id="ac-sch-order">
        <input
          id="ac-sch-order"
          v-model.number="scheduleForm.order"
          type="number"
          min="0"
          class="form-control"
          :class="{ 'is-invalid': scheduleErrors.order }"
        />
      </FormField>

      <FormField
        label="Branch"
        :error="scheduleErrors.branch"
        field-id="ac-sch-branch"
        hint="Leave blank for church-wide"
      >
        <select id="ac-sch-branch" v-model="scheduleForm.branch" class="form-select">
          <option :value="null">Church-wide</option>
          <option v-for="b in branches" :key="b.id" :value="b.id">{{ b.name }}</option>
        </select>
      </FormField>

      <template #footer>
        <button
          type="button"
          class="btn btn-alt-secondary btn-sm"
          @click="showScheduleCreate = false"
        >
          Cancel
        </button>
        <button
          type="button"
          class="btn btn-primary btn-sm"
          :disabled="creatingSchedule"
          @click="submitSchedule"
        >
          <span v-if="creatingSchedule" class="spinner-border spinner-border-sm me-1"></span>
          Add row
        </button>
      </template>
    </AppModal>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "../composables/useToast";
import aboutService from "../services/about.service";
import churchProfileService from "../services/church-profile.service";
import branchesService from "../services/branches.service";

const toast = useToast();
const branches = ref([]);

const tab = ref("profile");

const profile = ref({});
const loadingProfile = ref(true);
const savingProfile = ref(false);
const profileErrors = ref({});

const gallery = ref([]);
const showPhotoUpload = ref(false);
const uploadingPhoto = ref(false);
const selectedPhoto = ref(null);
const photoForm = ref({ caption: "", branch: null });
const photoErrors = ref({});

const facilities = ref([]);
const loadingFacilities = ref(true);
const showFacilityCreate = ref(false);
const creatingFacility = ref(false);
const facilityForm = ref({ name: "", description: "", branch: null });
const facilityErrors = ref({});

const schedule = ref([]);
const loadingSchedule = ref(true);
const showScheduleCreate = ref(false);
const creatingSchedule = ref(false);
const scheduleForm = ref({ name: "", day: "", time: "", order: 0, branch: null });
const scheduleErrors = ref({});

const facilityColumns = [
  { field: "name", header: "Name", sortable: true, strong: true },
  { field: "description", header: "Description" },
];

const scheduleColumns = [
  { field: "name", header: "Service", sortable: true, strong: true },
  { field: "day", header: "Day", sortable: true },
  { field: "time", header: "Time", sortable: true },
];

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

async function fetchProfile() {
  loadingProfile.value = true;
  try {
    const { data } = await churchProfileService.get();
    profile.value = data;
  } finally {
    loadingProfile.value = false;
  }
}

function validateProfile() {
  const e = {};
  if (!String(profile.value.name || "").trim()) e.name = "Church name is required.";
  const email = String(profile.value.email || "").trim();
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
    e.email = "Enter a valid email address.";
  profileErrors.value = e;
  return Object.keys(e).length === 0;
}

async function saveProfile() {
  if (!validateProfile()) return;

  savingProfile.value = true;
  try {
    const { data } = await churchProfileService.update(profile.value);
    profile.value = data;
    profileErrors.value = {};
    toast.add({ severity: "success", summary: "Church profile saved", life: 2500 });
  } catch (e) {
    const mapped = apiErrorMessages(e);
    profileErrors.value = { ...profileErrors.value, ...mapped };
    toast.add({
      severity: "error",
      summary: "Failed to save",
      detail: Object.values(mapped)[0] || e.message,
      life: 5000,
    });
  } finally {
    savingProfile.value = false;
  }
}

async function fetchGallery() {
  try {
    const { data } = await aboutService.listGallery();
    gallery.value = data.results || data;
  } catch {
    gallery.value = [];
  }
}

function openPhotoUpload() {
  photoForm.value = { caption: "", branch: null };
  selectedPhoto.value = null;
  photoErrors.value = {};
  showPhotoUpload.value = true;
}

function onPhotoChange(event) {
  selectedPhoto.value = event.target.files?.[0] || null;
}

function validatePhoto() {
  const e = {};
  if (!selectedPhoto.value) e.image = "Choose an image to upload.";
  photoErrors.value = e;
  return Object.keys(e).length === 0;
}

async function submitPhoto() {
  if (!validatePhoto()) return;

  uploadingPhoto.value = true;
  try {
    const fd = new FormData();
    fd.append("image", selectedPhoto.value);
    fd.append("caption", photoForm.value.caption);
    if (photoForm.value.branch) fd.append("branch", photoForm.value.branch);
    const { data } = await aboutService.uploadPhoto(fd);
    gallery.value.unshift(data);
    showPhotoUpload.value = false;
    selectedPhoto.value = null;
    photoForm.value = { caption: "", branch: null };
    photoErrors.value = {};
    toast.add({ severity: "success", summary: "Photo uploaded", life: 2500 });
  } catch (e) {
    const mapped = apiErrorMessages(e);
    photoErrors.value = { ...photoErrors.value, ...mapped };
    toast.add({
      severity: "error",
      summary: "Upload failed",
      detail: Object.values(mapped)[0] || e.message,
      life: 5000,
    });
  } finally {
    uploadingPhoto.value = false;
  }
}

async function fetchFacilities() {
  loadingFacilities.value = true;
  try {
    const { data } = await aboutService.listFacilities();
    facilities.value = data.results || data;
  } finally {
    loadingFacilities.value = false;
  }
}

function openFacilityCreate() {
  facilityForm.value = { name: "", description: "", branch: null };
  facilityErrors.value = {};
  showFacilityCreate.value = true;
}

function validateFacility() {
  const e = {};
  if (!String(facilityForm.value.name || "").trim()) e.name = "Facility name is required.";
  facilityErrors.value = e;
  return Object.keys(e).length === 0;
}

async function submitFacility() {
  if (!validateFacility()) return;

  creatingFacility.value = true;
  try {
    const { data } = await aboutService.createFacility(facilityForm.value);
    facilities.value.unshift(data);
    showFacilityCreate.value = false;
    facilityForm.value = { name: "", description: "", branch: null };
    facilityErrors.value = {};
    toast.add({ severity: "success", summary: "Facility created", life: 2500 });
  } catch (e) {
    const mapped = apiErrorMessages(e);
    facilityErrors.value = { ...facilityErrors.value, ...mapped };
    toast.add({
      severity: "error",
      summary: "Failed to create",
      detail: Object.values(mapped)[0] || e.message,
      life: 5000,
    });
  } finally {
    creatingFacility.value = false;
  }
}

async function fetchSchedule() {
  loadingSchedule.value = true;
  try {
    const { data } = await aboutService.listSchedule();
    schedule.value = data.results || data;
  } finally {
    loadingSchedule.value = false;
  }
}

function openScheduleCreate() {
  scheduleForm.value = { name: "", day: "", time: "", order: 0, branch: null };
  scheduleErrors.value = {};
  showScheduleCreate.value = true;
}

function validateSchedule() {
  const e = {};
  const f = scheduleForm.value;
  if (!String(f.name || "").trim()) e.name = "Service name is required.";
  if (!String(f.day || "").trim()) e.day = "Day is required.";
  if (!String(f.time || "").trim()) e.time = "Time is required.";
  if (f.order === "" || f.order === null || f.order === undefined || Number.isNaN(Number(f.order)))
    e.order = "Order is required.";
  else if (Number(f.order) < 0) e.order = "Order cannot be negative.";
  scheduleErrors.value = e;
  return Object.keys(e).length === 0;
}

async function submitSchedule() {
  if (!validateSchedule()) return;

  creatingSchedule.value = true;
  try {
    const { data } = await aboutService.createScheduleRow(scheduleForm.value);
    schedule.value.push(data);
    showScheduleCreate.value = false;
    scheduleForm.value = { name: "", day: "", time: "", order: 0, branch: null };
    scheduleErrors.value = {};
    toast.add({ severity: "success", summary: "Schedule row added", life: 2500 });
  } catch (e) {
    const mapped = apiErrorMessages(e);
    scheduleErrors.value = { ...scheduleErrors.value, ...mapped };
    toast.add({
      severity: "error",
      summary: "Failed to add",
      detail: Object.values(mapped)[0] || e.message,
      life: 5000,
    });
  } finally {
    creatingSchedule.value = false;
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

onMounted(() => {
  fetchProfile();
  fetchGallery();
  fetchFacilities();
  fetchSchedule();
  fetchBranches();
});
</script>

<style scoped>
/* Gallery is view-specific layout; shared form/header rules come from globals */
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
}
.gallery-item img {
  width: 100%;
  height: 140px;
  object-fit: cover;
  border-radius: 6px;
}
.gallery-caption {
  font-size: 0.8rem;
  color: var(--bs-secondary-color);
  margin-top: 0.35rem;
}
</style>
