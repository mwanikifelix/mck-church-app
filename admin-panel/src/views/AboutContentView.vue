<template>
  <Tabs value="0">
    <TabList>
      <Tab value="0">Church Profile</Tab>
      <Tab value="1">Gallery</Tab>
      <Tab value="2">Facilities</Tab>
      <Tab value="3">Service Schedule</Tab>
    </TabList>
    <TabPanels>
      <TabPanel value="0">
        <div class="panel-body" v-if="!loadingProfile">
          <div class="form-field">
            <label>Church Name</label>
            <InputText v-model="profile.name" class="w-full" />
          </div>
          <div class="form-field">
            <label>Tagline</label>
            <InputText v-model="profile.tagline" class="w-full" placeholder="e.g. Witnessing for Christ in Transforming lives" />
          </div>
          <div class="form-row">
            <div class="form-field">
              <label>Theme of the Year</label>
              <InputText v-model="profile.theme_title" class="w-full" />
            </div>
            <div class="form-field">
              <label>Scripture Reference</label>
              <InputText v-model="profile.theme_scripture_reference" class="w-full" placeholder="e.g. Genesis 8:1a" />
            </div>
          </div>
          <div class="form-field">
            <label>Theme Scripture Text</label>
            <Textarea v-model="profile.theme_scripture_text" class="w-full" rows="2" />
          </div>
          <div class="form-field">
            <label>Mission</label>
            <Textarea v-model="profile.mission" class="w-full" rows="2" />
          </div>
          <div class="form-field">
            <label>Vision</label>
            <Textarea v-model="profile.vision" class="w-full" rows="2" />
          </div>
          <div class="form-field">
            <label>Motto</label>
            <InputText v-model="profile.motto" class="w-full" />
          </div>
          <div class="form-row">
            <div class="form-field">
              <label>Email</label>
              <InputText v-model="profile.email" class="w-full" />
            </div>
            <div class="form-field">
              <label>Location</label>
              <InputText v-model="profile.location" class="w-full" />
            </div>
          </div>
          <Button label="Save Church Profile" :loading="savingProfile" @click="saveProfile" />
        </div>
      </TabPanel>

      <TabPanel value="1">
        <div class="header-row">
          <span></span>
          <Button label="Upload Photo" icon="pi pi-upload" @click="showPhotoUpload = true" />
        </div>
        <div class="gallery-grid">
          <div v-for="photo in gallery" :key="photo.id" class="gallery-item">
            <img :src="photo.image" :alt="photo.caption" />
            <div class="gallery-caption">{{ photo.caption }}</div>
          </div>
        </div>
      </TabPanel>

      <TabPanel value="2">
        <div class="header-row">
          <span></span>
          <Button label="New Facility" icon="pi pi-plus" @click="showFacilityCreate = true" />
        </div>
        <DataTable :value="facilities" :loading="loadingFacilities" paginator :rows="10">
          <Column field="name" header="Name" sortable />
          <Column field="description" header="Description" />
        </DataTable>
      </TabPanel>

      <TabPanel value="3">
        <div class="header-row">
          <span></span>
          <Button label="Add Row" icon="pi pi-plus" @click="showScheduleCreate = true" />
        </div>
        <DataTable :value="schedule" :loading="loadingSchedule" paginator :rows="15">
          <Column field="name" header="Service" sortable />
          <Column field="day" header="Day" sortable />
          <Column field="time" header="Time" sortable />
        </DataTable>
      </TabPanel>
    </TabPanels>
  </Tabs>

  <Dialog v-model:visible="showPhotoUpload" header="Upload Gallery Photo" modal style="width:420px">
    <div class="form-field">
      <label>Image</label>
      <FileUpload mode="basic" :auto="false" chooseLabel="Choose Image" accept="image/*" @select="onPhotoSelect" />
      <span v-if="selectedPhoto" class="file-name">{{ selectedPhoto.name }}</span>
    </div>
    <div class="form-field">
      <label>Caption</label>
      <InputText v-model="photoForm.caption" class="w-full" />
    </div>
    <div class="form-field">
      <label>Branch (optional)</label>
      <Select v-model="photoForm.branch" :options="branches" optionLabel="name" optionValue="id" class="w-full" showClear placeholder="Church-wide" />
    </div>
    <template #footer>
      <Button label="Cancel" text @click="showPhotoUpload = false" />
      <Button label="Upload" :loading="uploadingPhoto" @click="submitPhoto" />
    </template>
  </Dialog>

  <Dialog v-model:visible="showFacilityCreate" header="New Facility" modal style="width:420px">
    <div class="form-field">
      <label>Name</label>
      <InputText v-model="facilityForm.name" class="w-full" placeholder="e.g. Multi Purpose Hall" />
    </div>
    <div class="form-field">
      <label>Description</label>
      <Textarea v-model="facilityForm.description" class="w-full" rows="3" />
    </div>
    <div class="form-field">
      <label>Branch (optional)</label>
      <Select v-model="facilityForm.branch" :options="branches" optionLabel="name" optionValue="id" class="w-full" showClear placeholder="Church-wide" />
    </div>
    <template #footer>
      <Button label="Cancel" text @click="showFacilityCreate = false" />
      <Button label="Create" :loading="creatingFacility" @click="submitFacility" />
    </template>
  </Dialog>

  <Dialog v-model:visible="showScheduleCreate" header="New Schedule Row" modal style="width:420px">
    <div class="form-field">
      <label>Service Name</label>
      <InputText v-model="scheduleForm.name" class="w-full" placeholder="e.g. 1st Service" />
    </div>
    <div class="form-row">
      <div class="form-field">
        <label>Day</label>
        <InputText v-model="scheduleForm.day" class="w-full" placeholder="e.g. Sunday" />
      </div>
      <div class="form-field">
        <label>Time</label>
        <InputText v-model="scheduleForm.time" class="w-full" placeholder="e.g. 8:00AM" />
      </div>
    </div>
    <div class="form-field">
      <label>Order</label>
      <InputNumber v-model="scheduleForm.order" class="w-full" />
    </div>
    <div class="form-field">
      <label>Branch (optional)</label>
      <Select v-model="scheduleForm.branch" :options="branches" optionLabel="name" optionValue="id" class="w-full" showClear placeholder="Church-wide" />
    </div>
    <template #footer>
      <Button label="Cancel" text @click="showScheduleCreate = false" />
      <Button label="Create" :loading="creatingSchedule" @click="submitSchedule" />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Tabs from "primevue/tabs";
import TabList from "primevue/tablist";
import Tab from "primevue/tab";
import TabPanels from "primevue/tabpanels";
import TabPanel from "primevue/tabpanel";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import InputNumber from "primevue/inputnumber";
import Textarea from "primevue/textarea";
import Select from "primevue/select";
import FileUpload from "primevue/fileupload";
import { useToast } from "primevue/usetoast";
import aboutService from "../services/about.service";
import churchProfileService from "../services/church-profile.service";
import branchesService from "../services/branches.service";

const toast = useToast();
const branches = ref([]);

const profile = ref({});
const loadingProfile = ref(true);
const savingProfile = ref(false);

const gallery = ref([]);
const showPhotoUpload = ref(false);
const uploadingPhoto = ref(false);
const selectedPhoto = ref(null);
const photoForm = ref({ caption: "", branch: null });

const facilities = ref([]);
const loadingFacilities = ref(true);
const showFacilityCreate = ref(false);
const creatingFacility = ref(false);
const facilityForm = ref({ name: "", description: "", branch: null });

const schedule = ref([]);
const loadingSchedule = ref(true);
const showScheduleCreate = ref(false);
const creatingSchedule = ref(false);
const scheduleForm = ref({ name: "", day: "", time: "", order: 0, branch: null });

async function fetchProfile() {
  loadingProfile.value = true;
  try {
    const { data } = await churchProfileService.get();
    profile.value = data;
  } finally {
    loadingProfile.value = false;
  }
}

async function saveProfile() {
  savingProfile.value = true;
  try {
    const { data } = await churchProfileService.update(profile.value);
    profile.value = data;
    toast.add({ severity: "success", summary: "Church profile saved", life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Failed to save", detail: JSON.stringify(e.response?.data), life: 4000 });
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

function onPhotoSelect(event) {
  selectedPhoto.value = event.files[0];
}

async function submitPhoto() {
  if (!selectedPhoto.value) {
    toast.add({ severity: "warn", summary: "Choose an image first", life: 2500 });
    return;
  }
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
    toast.add({ severity: "success", summary: "Photo uploaded", life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Upload failed", detail: JSON.stringify(e.response?.data), life: 4000 });
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

async function submitFacility() {
  creatingFacility.value = true;
  try {
    const { data } = await aboutService.createFacility(facilityForm.value);
    facilities.value.unshift(data);
    showFacilityCreate.value = false;
    facilityForm.value = { name: "", description: "", branch: null };
    toast.add({ severity: "success", summary: "Facility created", life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Failed to create", detail: JSON.stringify(e.response?.data), life: 4000 });
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

async function submitSchedule() {
  creatingSchedule.value = true;
  try {
    const { data } = await aboutService.createScheduleRow(scheduleForm.value);
    schedule.value.push(data);
    showScheduleCreate.value = false;
    scheduleForm.value = { name: "", day: "", time: "", order: 0, branch: null };
    toast.add({ severity: "success", summary: "Schedule row added", life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Failed to add", detail: JSON.stringify(e.response?.data), life: 4000 });
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
.panel-body { max-width: 600px; padding: 1rem 0; }
.header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.form-field { margin-bottom: 1rem; }
.form-field label { display: block; margin-bottom: 0.35rem; font-size: 0.85rem; color: #475569; }
.form-row { display: flex; gap: 1rem; }
.form-row .form-field { flex: 1; }
.w-full { width: 100%; }
.file-name { display: block; margin-top: 0.5rem; font-size: 0.85rem; color: #475569; }
.gallery-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 1rem; }
.gallery-item img { width: 100%; height: 140px; object-fit: cover; border-radius: 6px; }
.gallery-caption { font-size: 0.8rem; color: #64748b; margin-top: 0.35rem; }
</style>
