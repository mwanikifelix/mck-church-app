<template>
  <DataTable :value="store.roles" :loading="store.loading" scrollable scrollHeight="70vh">
    <Column field="name" header="Role" frozen style="font-weight:600; min-width:180px;" />
    <Column v-for="perm in store.permissions" :key="perm.id" :header="perm.code" style="min-width:60px; text-align:center;">
      <template #body="{ data }">
        <Checkbox
          :modelValue="data.permissions.includes(perm.code)"
          binary
          :disabled="savingRoleId === data.id"
          @update:modelValue="(checked) => togglePermission(data, perm.code, checked)"
        />
      </template>
    </Column>
  </DataTable>
</template>

<script setup>
import { ref, onMounted } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Checkbox from "primevue/checkbox";
import { useToast } from "primevue/usetoast";
import { useRolesStore } from "../store/roles";
import rolesService from "../services/roles.service";

const store = useRolesStore();
const toast = useToast();
const savingRoleId = ref(null);

onMounted(() => store.fetchAll());

async function togglePermission(role, code, checked) {
  const previous = role.permissions;
  const newCodes = checked ? [...previous, code] : previous.filter((c) => c !== code);
  role.permissions = newCodes;

  savingRoleId.value = role.id;
  try {
    const { data } = await rolesService.setPermissions(role.id, newCodes);
    role.permissions = data.permissions;
  } catch (e) {
    role.permissions = previous;
    toast.add({ severity: "error", summary: `Failed to update ${role.name}`, life: 3000 });
  } finally {
    savingRoleId.value = null;
  }
}
</script>
