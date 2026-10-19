<template>
  <div>
    <!-- Header -->
    <BasePageHeading
      title="Roles &amp; Permissions"
      icon="fa-user-shield"
      tone="dark"
      :subtitle="`${store.roles.length} roles · ${store.permissions.length} permissions`"
    >
      <template #extra>
        <button
          type="button"
          class="btn btn-light btn-sm"
          :disabled="store.loading"
          @click="store.fetchAll()"
        >
          <i class="fa fa-sync-alt me-1" :class="{ 'fa-spin': store.loading }"></i>
          Refresh
        </button>
      </template>
    </BasePageHeading>

    <div class="content">
    <div v-if="store.loading" class="block rounded-3">
      <div class="block-content text-center py-5">
        <div class="spinner-border text-primary mb-3"></div>
        <p class="text-muted mb-0">Loading roles and permissions…</p>
      </div>
    </div>

    <div v-else-if="!store.roles.length" class="block rounded-3">
      <div class="block-content text-center py-5">
        <i class="fa fa-user-shield fa-2x opacity-25 mb-2 d-block"></i>
        <p class="text-muted mb-0">No roles defined yet.</p>
      </div>
    </div>

    <template v-else>
      <!-- Role summary cards -->
      <div class="row g-3 mb-4">
        <div
          v-for="role in store.roles"
          :key="role.id"
          class="col-12 col-sm-6 col-xl-4"
        >
          <div class="block rounded-3 h-100">
            <div class="block-content p-3">
              <div class="d-flex align-items-start justify-content-between gap-2">
                <div class="min-w-0">
                  <div class="fw-bold text-truncate">{{ role.name }}</div>
                  <div class="fs-sm text-muted">
                    {{ role.permissions.length }} of
                    {{ store.permissions.length }} permissions granted
                  </div>
                </div>
                <span
                  class="badge rounded-pill flex-shrink-0"
                  :class="
                    role.permissions.length === store.permissions.length
                      ? 'bg-success-subtle text-success-emphasis'
                      : 'bg-primary-subtle text-primary-emphasis'
                  "
                >
                  {{ Math.round((role.permissions.length / (store.permissions.length || 1)) * 100) }}%
                </span>
              </div>

              <!-- Grant progress -->
              <div
                class="progress mt-3"
                style="height: 5px"
                role="progressbar"
                :aria-valuenow="role.permissions.length"
                aria-valuemin="0"
                :aria-valuemax="store.permissions.length"
              >
                <div
                  class="progress-bar"
                  :style="{
                    width:
                      (role.permissions.length / (store.permissions.length || 1)) * 100 + '%',
                  }"
                ></div>
              </div>

              <!-- Top granted capabilities -->
              <div class="d-flex flex-wrap gap-1 mt-2">
                <span
                  v-for="code in topPermissions(role)"
                  :key="code"
                  class="badge rounded-pill bg-light text-dark border fs-xs"
                >
                  {{ code }}
                </span>
                <span
                  v-if="role.permissions.length > 3"
                  class="badge rounded-pill bg-light text-muted border fs-xs"
                >
                  +{{ role.permissions.length - 3 }} more
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Permission matrix, grouped by domain -->
      <div class="block rounded-3">
        <div
          class="block-header d-flex flex-column flex-sm-row gap-2 align-items-sm-center justify-content-between"
        >
          <div>
            <span class="block-title fw-bold d-block">Permission matrix</span>
            <span class="fs-sm text-muted">
              Toggle a checkbox to grant or revoke. Changes save immediately.
            </span>
          </div>
          <span
            v-if="dirtyCount"
            class="badge rounded-pill bg-warning-subtle text-warning-emphasis"
          >
            <i class="fa fa-circle-notch fa-spin me-1"></i>
            Saving {{ dirtyCount }} change{{ dirtyCount > 1 ? "s" : "" }}…
          </span>
        </div>

        <div class="block-content p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0 perm-table">
              <thead>
                <tr>
                  <th scope="col" class="perm-role-col">Role</th>
                  <th
                    v-for="group in permissionGroups"
                    :key="group.key"
                    scope="colgroup"
                    :colspan="group.items.length"
                    class="text-center perm-group-head"
                    :class="`text-${group.tone}`"
                  >
                    {{ group.label }}
                  </th>
                </tr>
                <tr>
                  <th scope="col" class="perm-role-col">—</th>
                  <th
                    v-for="perm in flatPermissions"
                    :key="perm.id"
                    scope="col"
                    class="text-center perm-col"
                    :title="perm.description || perm.code"
                  >
                    <span class="perm-code" :title="perm.code">
                      {{ shortCode(perm.code) }}
                    </span>
                  </th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="role in store.roles" :key="role.id">
                  <th scope="row" class="perm-role-col fw-semibold">
                    {{ role.name }}
                  </th>
                  <td
                    v-for="perm in flatPermissions"
                    :key="perm.id"
                    class="text-center"
                    :class="{ 'bg-primary-subtle': savingRoleId === role.id }"
                  >
                    <div class="form-check d-inline-block m-0">
                      <input
                        class="form-check-input"
                        type="checkbox"
                        role="checkbox"
                        :checked="role.permissions.includes(perm.code)"
                        :aria-label="`${role.name}: ${perm.code}`"
                        :disabled="savingRoleId === role.id"
                        @change="
                          (e) => togglePermission(role, perm.code, e.target.checked)
                        "
                      />
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useToast } from "../composables/useToast";
import { useRolesStore } from "../store/roles";
import rolesService from "../services/roles.service";

const store = useRolesStore();
const toast = useToast();
const savingRoleId = ref(null);
const dirtyCount = ref(0);

/**
 * Group permission codes by their domain prefix ("youth.manage" -> "youth")
 * so the matrix reads as sections rather than one undifferentiated strip.
 */
const GROUP_LABELS = {
  members: { label: "Members", tone: "primary" },
  membership: { label: "Members", tone: "primary" },
  youth: { label: "Groups", tone: "info" },
  groups: { label: "Groups", tone: "info" },
  hbc: { label: "Groups", tone: "info" },
  events: { label: "Engagement", tone: "success" },
  announcements: { label: "Engagement", tone: "success" },
  content: { label: "Content", tone: "warning" },
  giving: { label: "Finance", tone: "danger" },
  finance: { label: "Finance", tone: "danger" },
  pastoral: { label: "Care", tone: "secondary" },
  prayer: { label: "Care", tone: "secondary" },
  branches: { label: "Structure", tone: "dark" },
  departments: { label: "Structure", tone: "dark" },
  roles: { label: "Administration", tone: "dark" },
  accounts: { label: "Administration", tone: "dark" },
  registration: { label: "Administration", tone: "dark" },
};

const permissionGroups = computed(() => {
  const map = new Map();
  store.permissions.forEach((perm) => {
    const key = (perm.code || "").split(".")[0];
    const meta = GROUP_LABELS[key] || { label: "Other", tone: "secondary" };
    const bucket = key;
    if (!map.has(bucket)) {
      map.set(bucket, { key: bucket, label: meta.label, tone: meta.tone, items: [] });
    }
    map.get(bucket).items.push(perm);
  });

  // Merge buckets that share a label so each domain is one contiguous block
  const merged = new Map();
  map.forEach((g) => {
    if (!merged.has(g.label)) {
      merged.set(g.label, { key: g.label, label: g.label, tone: g.tone, items: [] });
    }
    merged.get(g.label).items.push(...g.items);
  });
  return [...merged.values()];
});

const flatPermissions = computed(() => permissionGroups.value.flatMap((g) => g.items));

function shortCode(code) {
  // "youth.manage" -> "manage", prefixed when ambiguous
  const [, action] = String(code).split(".");
  return action || code;
}

function topPermissions(role) {
  return role.permissions.slice(0, 3);
}

async function togglePermission(role, code, checked) {
  const previous = role.permissions;
  const newCodes = checked ? [...previous, code] : previous.filter((c) => c !== code);
  role.permissions = newCodes;

  dirtyCount.value += 1;
  savingRoleId.value = role.id;
  try {
    const { data } = await rolesService.setPermissions(role.id, newCodes);
    role.permissions = data.permissions;
  } catch {
    role.permissions = previous;
    toast.add({
      severity: "error",
      summary: `Could not update ${role.name}`,
      detail: "Your change was rolled back.",
      life: 4000,
    });
  } finally {
    dirtyCount.value = Math.max(0, dirtyCount.value - 1);
    if (!dirtyCount.value) savingRoleId.value = null;
  }
}

onMounted(() => store.fetchAll());
</script>

<style scoped>
.min-w-0 {
  min-width: 0;
}
.perm-table thead th {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  white-space: nowrap;
  background-color: var(--bs-body-bg);
}
.perm-group-head {
  border-left: 1px solid var(--bs-border-color);
  font-weight: 700;
}
.perm-role-col {
  min-width: 10rem;
  position: sticky;
  left: 0;
  background-color: var(--bs-body-bg);
  z-index: 1;
  text-align: left !important;
}
.perm-col {
  min-width: 3.25rem;
  border-left: 1px solid var(--bs-border-color);
}
.perm-code {
  font-size: 0.65rem;
  opacity: 0.65;
  cursor: help;
}
</style>
