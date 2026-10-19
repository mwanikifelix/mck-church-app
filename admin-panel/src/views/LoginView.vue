<template>
  <div class="login-page">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100 py-4">
        <div class="col-12 col-sm-9 col-md-7 col-lg-5 col-xl-4">
          <!-- Brand -->
          <div class="text-center mb-4">
            <span
              class="d-inline-flex align-items-center justify-content-center rounded-circle bg-primary text-white mb-3"
              style="width: 3.5rem; height: 3.5rem"
            >
              <i class="fa fa-church fa-lg"></i>
            </span>
            <h1 class="h4 fw-bold mb-1">MCK Wesley Church</h1>
            <p class="text-muted mb-0">Administration Panel</p>
          </div>

          <!-- Card -->
          <div class="block rounded-3 shadow-sm">
            <div class="block-header">
              <span class="block-title fw-bold">Sign in</span>
              <span class="fs-sm text-muted">Use your church account</span>
            </div>

            <div class="block-content p-4">
              <form novalidate @submit.prevent="handleLogin">
                <FormField label="Email address" required field-id="login-email">
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="fa fa-envelope opacity-50"></i>
                    </span>
                    <input
                      id="login-email"
                      v-model.trim="email"
                      type="email"
                      class="form-control"
                      placeholder="name@example.com"
                      autocomplete="username"
                      required
                    />
                  </div>
                </FormField>

                <FormField label="Password" required field-id="login-password">
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="fa fa-lock opacity-50"></i>
                    </span>
                    <input
                      id="login-password"
                      v-model="password"
                      :type="showPassword ? 'text' : 'password'"
                      class="form-control"
                      placeholder="••••••••"
                      autocomplete="current-password"
                      required
                    />
                    <button
                      class="btn btn-outline-secondary"
                      type="button"
                      :aria-label="showPassword ? 'Hide password' : 'Show password'"
                      @click="showPassword = !showPassword"
                    >
                      <i class="fa" :class="showPassword ? 'fa-eye-slash' : 'fa-eye'"></i>
                    </button>
                  </div>
                </FormField>

                <div v-if="error" class="alert alert-danger py-2 fs-sm" role="alert">
                  <i class="fa fa-exclamation-circle me-1"></i>
                  {{ error }}
                </div>

                <button
                  type="submit"
                  class="btn btn-primary w-100"
                  :disabled="loading"
                >
                  <span
                    v-if="loading"
                    class="spinner-border spinner-border-sm me-2"
                  ></span>
                  <i v-else class="fa fa-sign-in-alt me-2"></i>
                  {{ loading ? "Signing in…" : "Sign in" }}
                </button>
              </form>
            </div>
          </div>

          <p class="text-center text-muted fs-sm mt-4 mb-0">
            MCK Wesley Church &copy; {{ year }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../store/auth";
import FormField from "../components/FormField.vue";

const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);
const showPassword = ref(false);

const router = useRouter();
const auth = useAuthStore();
const year = computed(() => new Date().getFullYear());

async function handleLogin() {
  error.value = "";

  if (!email.value) {
    error.value = "Enter your email address.";
    return;
  }
  if (!password.value) {
    error.value = "Enter your password.";
    return;
  }

  loading.value = true;
  try {
    await auth.login(email.value, password.value);
    router.push({ name: "dashboard" });
  } catch (e) {
    error.value =
      e.response?.data?.detail ||
      e.response?.data?.email ||
      e.response?.data?.password ||
      (e.message === "Network Error"
        ? "Cannot reach the server. Please try again shortly."
        : "Sign in failed. Check your credentials.");
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background:
    radial-gradient(circle at 15% 20%, rgba(11, 107, 216, 0.18), transparent 45%),
    radial-gradient(circle at 85% 80%, rgba(100, 164, 42, 0.16), transparent 45%),
    var(--bs-body-bg);
}
</style>
