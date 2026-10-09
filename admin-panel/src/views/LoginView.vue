<template>
  <div class="login-page">
    <Card class="login-card">
      <template #title>MCK Wesley Admin</template>
      <template #subtitle>Sign in to manage the church system</template>
      <template #content>
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="field">
            <label>Email</label>
            <InputText v-model="email" type="email" required class="w-full" />
          </div>
          <div class="field">
            <label>Password</label>
            <Password v-model="password" :feedback="false" toggleMask required class="w-full" inputClass="w-full" />
          </div>
          <Message v-if="error" severity="error" :closable="false">{{ error }}</Message>
          <Button type="submit" label="Log In" :loading="loading" class="w-full" />
        </form>
      </template>
    </Card>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../store/auth";
import Card from "primevue/card";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import Button from "primevue/button";
import Message from "primevue/message";

const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);
const router = useRouter();
const auth = useAuthStore();

async function handleLogin() {
  loading.value = true;
  error.value = "";
  try {
    await auth.login(email.value, password.value);
    router.push({ name: "dashboard" });
  } catch (e) {
    error.value = e.response?.data?.detail || "Login failed.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f4f6f9;
}
.login-card {
  width: 380px;
}
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.field label {
  display: block;
  margin-bottom: 0.35rem;
  font-size: 0.85rem;
  color: #475569;
}
.w-full {
  width: 100%;
}
</style>
