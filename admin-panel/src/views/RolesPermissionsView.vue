<template>
  <NavBar />
  <div style="padding:2rem; font-family:sans-serif;">
    <h1>Roles & Permissions</h1>
    <p v-if="store.loading">Loading...</p>
    <p v-if="saveError" style="color:red;">{{ saveError }}</p>

    <div v-if="!store.loading" style="overflow-x:auto;">
      <table border="1" cellpadding="6" style="border-collapse:collapse; white-space:nowrap;">
        <thead>
          <tr>
            <th style="position:sticky; left:0; background:#fff; text-align:left;">Role</th>
            <th
              v-for="perm in store.permissions"
              :key="perm.id"
              :title="perm.description"
              style="writing-mode:vertical-rl; text-orientation:mixed; font-weight:normal; font-size:0.8rem;"
            >
              {{ perm.code }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="role in store.roles" :key="role.id">
            <td style="position:sticky; left:0; background:#fff; font-weight:bold;">
              {{ role.name }}
              <span v-if="savingRoleId === role.id" style="font-weight:normal; color:#888;"> (saving...)</span>
            </td>
            <td v-for="perm in store.permissions" :key="perm.id" style="text-align:center;">
              <input
                type="checkbox"
                :checked="role.permissions.includes(perm.code)"
                :disabled="savingRoleId === role.id"
                @change="togglePermission(role, perm.code, $event.target.checked)"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import NavBar from "../components/NavBar.vue";
import { useRolesStore } from "../store/roles";
import rolesService from "../services/roles.service";

const store = useRolesStore();
const savingRoleId = ref(null);
const saveError = ref("");

onMounted(() => store.fetchAll());

async function togglePermission(role, code, checked) {
  const currentCodes = role.permissions;
  const newCodes = checked
    ? [...currentCodes, code]
    : currentCodes.filter((c) => c !== code);

  // Optimistic update
  const previous = role.permissions;
  role.permissions = newCodes;

  savingRoleId.value = role.id;
  saveError.value = "";
  try {
    const { data } = await rolesService.setPermissions(role.id, newCodes);
    role.permissions = data.permissions;
  } catch (e) {
    role.permissions = previous; // revert on failure
    saveError.value = e.response?.data?.detail || `Failed to update ${role.name}.`;
  } finally {
    savingRoleId.value = null;
  }
}
</script>
