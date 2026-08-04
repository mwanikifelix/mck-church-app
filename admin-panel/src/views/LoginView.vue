<template>
  <div style="max-width:360px; margin:4rem auto; font-family:sans-serif;">
    <h2>MCK Admin Login</h2>
    <form @submit.prevent="handleLogin">
      <div style="margin-bottom:1rem;">
        <label>Email</label>
        <input v-model="email" type="email" required style="width:100%; padding:0.5rem;" />
      </div>
      <div style="margin-bottom:1rem;">
        <label>Password</label>
        <input v-model="password" type="password" required style="width:100%; padding:0.5rem;" />
      </div>
      <p v-if="error" style="color:red;">{{ error }}</p>
      <button type="submit" :disabled="loading" style="width:100%; padding:0.6rem;">
        {{ loading ? "Logging in..." : "Log In" }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../store/auth";

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
