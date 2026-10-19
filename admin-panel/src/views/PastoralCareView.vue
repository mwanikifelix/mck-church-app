<template>
  <div>
    <BasePageHeading
      title="Pastoral Care"
      icon="fa-hands-helping"
      subtitle="Prayer and counselling follow-up for the congregation"
    />

    <div class="content">
    <!-- Prayer requests -->
    <h2 class="section-title mb-3">Prayer Requests</h2>
    <AppDataTable
      class="mb-4"
      :rows="prayerRequests"
      :columns="prayerColumns"
      :loading="loadingPrayer"
      :page-size="10"
      :search-fields="prayerSearchFields"
      search-placeholder="Search prayer requests…"
      export-name="prayer-requests"
      empty-text="No prayer requests yet."
      empty-icon="fa-heart"
    >
      <template #from="{ row }">{{ row.submitter_name || "Anonymous" }}</template>

      <template #status="{ row }">
        <span class="badge rounded-pill" :class="prayerStatusClass(row.status)">
          <i class="fa fa-circle me-1" style="font-size: 0.5rem; vertical-align: middle"></i>
          {{ row.status }}
        </span>
      </template>

      <!--
        `#actions` doubles as AppDataTable's toolbar slot, so the content must
        stay guarded on `row` — the toolbar invokes it without row props.
      -->
      <template #actions="{ row }">
        <div v-if="row" class="d-flex gap-2 justify-content-end">
          <button
            v-if="row.status !== 'answered' && $can('prayer.manage')"
            type="button"
            class="btn btn-primary btn-sm"
            :disabled="rowBusy(row.id)"
            @click="answerPrayer(row)"
          >
            <span
              v-if="busy(row.id, 'answer')"
              class="spinner-border spinner-border-sm me-1"
            ></span>
            Mark Answered
          </button>
        </div>
      </template>
    </AppDataTable>

    <!-- Counselling requests -->
    <h2 class="section-title mb-3">Counselling Requests</h2>
    <AppDataTable
      :rows="counsellingRequests"
      :columns="counsellingColumns"
      :loading="loadingCounselling"
      :page-size="10"
      search-placeholder="Search counselling requests…"
      export-name="counselling-requests"
      empty-text="No counselling requests yet."
      empty-icon="fa-hands-helping"
    >
      <template #status="{ row }">
        <span class="badge rounded-pill" :class="counsellingStatusClass(row.status)">
          <i class="fa fa-circle me-1" style="font-size: 0.5rem; vertical-align: middle"></i>
          {{ row.status }}
        </span>
      </template>

      <template #confirmed="{ row }">
        {{ row.confirmed_datetime ? new Date(row.confirmed_datetime).toLocaleString() : "—" }}
      </template>

      <template #counsellor="{ row }">{{ row.counsellor_name || "—" }}</template>

      <template #actions="{ row }">
        <!-- Counselling status changes need pastoral.view_all on the backend -->
        <div
          v-if="row && $can('pastoral.view_all')"
          class="d-flex gap-2 justify-content-end flex-wrap"
        >
          <button
            v-if="row.status === 'pending'"
            type="button"
            class="btn btn-primary btn-sm"
            :disabled="rowBusy(row.id)"
            @click="openConfirmDialog(row)"
          >
            <span v-if="busy(row.id, 'confirm')" class="spinner-border spinner-border-sm me-1"></span>
            Confirm
          </button>
          <button
            v-if="row.status === 'confirmed'"
            type="button"
            class="btn btn-success btn-sm"
            :disabled="rowBusy(row.id)"
            @click="setStatus(row, 'completed', 'complete')"
          >
            <span
              v-if="busy(row.id, 'complete')"
              class="spinner-border spinner-border-sm me-1"
            ></span>
            Mark Completed
          </button>
          <button
            v-if="row.status !== 'completed' && row.status !== 'cancelled'"
            type="button"
            class="btn btn-outline-danger btn-sm"
            :disabled="rowBusy(row.id)"
            @click="setStatus(row, 'cancelled', 'cancel')"
          >
            <span v-if="busy(row.id, 'cancel')" class="spinner-border spinner-border-sm me-1"></span>
            Cancel
          </button>
        </div>
      </template>
    </AppDataTable>

    <!-- Confirm counselling request dialog -->
    <AppModal
      v-model:visible="showConfirm"
      title="Confirm Counselling Request"
      subtitle="Pick a date and time for the session"
    >
      <FormField
        label="Date & Time"
        required
        :error="errors.confirmed_datetime"
        field-id="pc-when"
      >
        <input
          id="pc-when"
          v-model="confirmForm.confirmed_datetime"
          type="datetime-local"
          class="form-control"
          :class="{ 'is-invalid': errors.confirmed_datetime }"
        />
      </FormField>

      <FormField
        label="Assigned Counsellor"
        :error="errors.counsellor"
        field-id="pc-counsellor"
        hint="Optional — assign a member to follow up"
      >
        <select
          id="pc-counsellor"
          v-model="confirmForm.counsellor"
          class="form-select"
          :class="{ 'is-invalid': errors.counsellor }"
        >
          <option :value="null">Unassigned</option>
          <option v-for="m in members" :key="m.id" :value="m.id">
            {{ m.full_name }}
          </option>
        </select>
      </FormField>

      <FormField label="Notes" :error="errors.admin_notes" field-id="pc-notes">
        <textarea
          id="pc-notes"
          v-model="confirmForm.admin_notes"
          rows="2"
          class="form-control"
          :class="{ 'is-invalid': errors.admin_notes }"
        ></textarea>
      </FormField>

      <template #footer>
        <button type="button" class="btn btn-alt-secondary btn-sm" @click="showConfirm = false">
          Cancel
        </button>
        <button
          type="button"
          class="btn btn-primary btn-sm"
          :disabled="confirming"
          @click="submitConfirm"
        >
          <span v-if="confirming" class="spinner-border spinner-border-sm me-1"></span>
          Confirm request
        </button>
      </template>
    </AppModal>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "../composables/useToast";
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
const errors = ref({});

// Row-level busy state: which row id + which button is in flight
const acting = ref(null);
const actingAction = ref("");

const prayerColumns = [
  { field: "submitter_name", header: "From", slot: "from" },
  { field: "body", header: "Request", sortable: true },
  { field: "status", header: "Status", slot: "status" },
  { field: "support_count", header: "Supporters", sortable: true },
  { header: "Actions", slot: "actions", align: "end", sortable: false },
];
// Anonymous prayers have no submitter_name, so search them by their fallback too
const prayerSearchFields = [
  "submitter_name",
  "body",
  "status",
  "support_count",
  (r) => r.submitter_name || "Anonymous",
];

const counsellingColumns = [
  { field: "user_name", header: "Member", sortable: true, strong: true },
  { field: "message", header: "Message" },
  { field: "status", header: "Status", slot: "status" },
  { field: "confirmed_datetime", header: "Confirmed Time", slot: "confirmed" },
  { field: "counsellor_name", header: "Counsellor", slot: "counsellor" },
  { header: "Actions", slot: "actions", align: "end", sortable: false },
];

function prayerStatusClass(status) {
  if (status === "answered") return "bg-success-subtle text-success-emphasis";
  if (status === "pending") return "bg-warning-subtle text-warning-emphasis";
  return "bg-info-subtle text-info-emphasis";
}

function counsellingStatusClass(status) {
  if (status === "completed") return "bg-success-subtle text-success-emphasis";
  if (status === "confirmed") return "bg-info-subtle text-info-emphasis";
  if (status === "pending") return "bg-warning-subtle text-warning-emphasis";
  if (status === "cancelled") return "bg-danger-subtle text-danger-emphasis";
  return "bg-secondary-subtle text-secondary-emphasis";
}

function busy(rowId, action) {
  return acting.value === rowId && actingAction.value === action;
}

function rowBusy(rowId) {
  return acting.value === rowId;
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
  acting.value = p.id;
  actingAction.value = "answer";
  try {
    await prayerService.markAnswered(p.id);
    p.status = "answered";
    toast.add({ severity: "success", summary: "Marked as answered", life: 2000 });
  } catch (e) {
    const mapped = apiErrorMessages(e);
    toast.add({
      severity: "error",
      summary: "Action failed",
      detail: Object.values(mapped)[0] || e.message,
      life: 5000,
    });
  } finally {
    acting.value = null;
    actingAction.value = "";
  }
}

function openConfirmDialog(request) {
  activeRequest.value = request;
  confirmForm.value = { confirmed_datetime: null, counsellor: null, admin_notes: "" };
  errors.value = {};
  showConfirm.value = true;
}

function validateConfirm() {
  const e = {};
  if (!confirmForm.value.confirmed_datetime)
    e.confirmed_datetime = "Date and time are required.";
  errors.value = e;
  return Object.keys(e).length === 0;
}

async function submitConfirm() {
  if (!validateConfirm()) return;

  confirming.value = true;
  try {
    // datetime-local gives "YYYY-MM-DDTHH:mm"; the API expects an ISO string
    const when = new Date(confirmForm.value.confirmed_datetime);
    const payload = {
      status: "confirmed",
      confirmed_datetime: Number.isNaN(when.getTime()) ? undefined : when.toISOString(),
      counsellor: confirmForm.value.counsellor,
      admin_notes: confirmForm.value.admin_notes,
    };
    const { data } = await pastoralService.updateCounselling(activeRequest.value.id, payload);
    Object.assign(activeRequest.value, data);
    showConfirm.value = false;
    toast.add({ severity: "success", summary: "Request confirmed", life: 2500 });
  } catch (e) {
    const mapped = apiErrorMessages(e);
    errors.value = { ...errors.value, ...mapped };
    toast.add({
      severity: "error",
      summary: "Failed to confirm",
      detail: Object.values(mapped)[0] || e.message,
      life: 5000,
    });
  } finally {
    confirming.value = false;
  }
}

async function setStatus(request, status, action) {
  acting.value = request.id;
  actingAction.value = action;
  try {
    const { data } = await pastoralService.updateCounselling(request.id, { status });
    Object.assign(request, data);
    toast.add({ severity: "success", summary: `Marked ${status}`, life: 2000 });
  } catch (e) {
    const mapped = apiErrorMessages(e);
    toast.add({
      severity: "error",
      summary: "Action failed",
      detail: Object.values(mapped)[0] || e.message,
      life: 5000,
    });
  } finally {
    acting.value = null;
    actingAction.value = "";
  }
}

onMounted(() => {
  fetchPrayer();
  fetchCounselling();
  fetchMembers();
});
</script>
