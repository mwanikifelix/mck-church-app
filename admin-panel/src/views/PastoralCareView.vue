<template>
  <div>
    <h2 class="section-title">Prayer Requests</h2>
    <DataTable :value="prayerRequests" :loading="loadingPrayer" paginator :rows="10" class="mb-4">
      <Column header="From"><template #body="{ data }">{{ data.submitter_name || "Anonymous" }}</template></Column>
      <Column field="body" header="Request" />
      <Column field="status" header="Status">
        <template #body="{ data }">
          <Tag :value="data.status" :severity="data.status === 'answered' ? 'success' : 'warn'" />
        </template>
      </Column>
      <Column field="support_count" header="Supporters" />
      <Column header="Actions">
        <template #body="{ data }">
          <Button v-if="data.status !== 'answered'" label="Mark Answered" size="small" @click="answerPrayer(data)" />
        </template>
      </Column>
    </DataTable>

    <h2 class="section-title">Counselling Requests</h2>
    <DataTable :value="counsellingRequests" :loading="loadingCounselling" paginator :rows="10">
      <Column header="Member"><template #body="{ data }">{{ data.user_name }}</template></Column>
      <Column field="message" header="Message" />
      <Column header="Status">
        <template #body="{ data }">
          <Tag :value="data.status" :severity="counsellingSeverity(data.status)" />
        </template>
      </Column>
      <Column header="Confirmed Time">
        <template #body="{ data }">{{ data.confirmed_datetime ? new Date(data.confirmed_datetime).toLocaleString() : "-" }}</template>
      </Column>
      <Column header="Counsellor">
        <template #body="{ data }">{{ data.counsellor_name || "-" }}</template>
      </Column>
      <Column header="Actions">
        <template #body="{ data }">
          <Button
            v-if="data.status === 'pending'"
            label="Confirm"
            size="small"
            class="mr-2"
            @click="openConfirmDialog(data)"
          />
          <Button
            v-if="data.status === 'confirmed'"
            label="Mark Completed"
            size="small"
            severity="success"
            class="mr-2"
            @click="setStatus(data, 'completed')"
          />
          <Button
            v-if="data.status !== 'completed' && data.status !== 'cancelled'"
            label="Cancel"
            size="small"
            severity="danger"
            outlined
            @click="setStatus(data, 'cancelled')"
          />
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="showConfirm" header="Confirm Counselling Request" modal style="width:420px">
      <div class="form-field">
        <label>Date &amp; Time</label>
        <DatePicker v-model="confirmForm.confirmed_datetime" showTime hourFormat="12" class="w-full" />
      </div>
      <div class="form-field">
        <label>Assigned Counsellor</label>
        <Select v-model="confirmForm.counsellor" :options="members" optionLabel="full_name" optionValue="id" filter class="w-full" placeholder="Select a member" />
      </div>
      <div class="form-field">
        <label>Notes</label>
        <Textarea v-model="confirmForm.admin_notes" class="w-full" rows="2" />
      </div>
      <template #footer>
        <Button label="Cancel" text @click="showConfirm = false" />
        <Button label="Confirm" :loading="confirming" @click="submitConfirm" />
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
import DatePicker from "primevue/datepicker";
import Select from "primevue/select";
import Textarea from "primevue/textarea";
import { useToast } from "primevue/usetoast";
import prayerService from "../services/prayer.service";
import pastoralService from "../services/pastoral.service";
import membersService from "../services/members.service";

const toast = useToast();
const prayerRequests = ref([]);
const counsellingRequests = ref([]);
const members = ref([]);
const loadingPrayer = ref(true);
const loadingCounselling = ref(true);
const showConfirm = ref(false);
const confirming = ref(false);
const activeRequest = ref(null);
const confirmForm = ref({ confirmed_datetime: null, counsellor: null, admin_notes: "" });

function counsellingSeverity(status) {
  if (status === "completed") return "success";
  if (status === "confirmed") return "info";
  if (status === "cancelled") return "danger";
  return "warn";
}

async function fetchPrayer() {
  loadingPrayer.value = true;
  try {
    const { data } = await prayerService.list();
    prayerRequests.value = data.results || data;
  } finally {
    loadingPrayer.value = false;
  }
}

async function fetchCounselling() {
  loadingCounselling.value = true;
  try {
    const { data } = await pastoralService.listCounselling();
    counsellingRequests.value = data.results || data;
  } finally {
    loadingCounselling.value = false;
  }
}

async function fetchMembers() {
  try {
    const { data } = await membersService.list();
    members.value = data.results || data;
  } catch {
    members.value = [];
  }
}

async function answerPrayer(p) {
  await prayerService.markAnswered(p.id);
  p.status = "answered";
  toast.add({ severity: "success", summary: "Marked as answered", life: 2000 });
}

function openConfirmDialog(request) {
  activeRequest.value = request;
  confirmForm.value = { confirmed_datetime: null, counsellor: null, admin_notes: "" };
  showConfirm.value = true;
}

async function submitConfirm() {
  confirming.value = true;
  try {
    const payload = {
      status: "confirmed",
      confirmed_datetime: confirmForm.value.confirmed_datetime?.toISOString(),
      counsellor: confirmForm.value.counsellor,
      admin_notes: confirmForm.value.admin_notes,
    };
    const { data } = await pastoralService.updateCounselling(activeRequest.value.id, payload);
    Object.assign(activeRequest.value, data);
    showConfirm.value = false;
    toast.add({ severity: "success", summary: "Request confirmed", life: 2500 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Failed to confirm", detail: JSON.stringify(e.response?.data), life: 4000 });
  } finally {
    confirming.value = false;
  }
}

async function setStatus(request, status) {
  try {
    const { data } = await pastoralService.updateCounselling(request.id, { status });
    Object.assign(request, data);
    toast.add({ severity: "success", summary: `Marked ${status}`, life: 2000 });
  } catch (e) {
    toast.add({ severity: "error", summary: "Action failed", detail: JSON.stringify(e.response?.data), life: 4000 });
  }
}

onMounted(() => {
  fetchPrayer();
  fetchCounselling();
  fetchMembers();
});
</script>

<style scoped>
.section-title { font-size: 1.1rem; font-weight: 600; margin: 0 0 0.75rem; color: #1e293b; }
.mb-4 { margin-bottom: 2rem; }
.mr-2 { margin-right: 0.5rem; }
.form-field { margin-bottom: 1rem; }
.form-field label { display: block; margin-bottom: 0.35rem; font-size: 0.85rem; color: #475569; }
.w-full { width: 100%; }
</style>
