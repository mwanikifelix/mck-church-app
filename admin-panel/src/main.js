import { createApp } from "vue";
import { createPinia } from "pinia";

// OneUI design system (Bootstrap 5) + Wesley brand theme
import "./styles.scss";

import App from "./App.vue";
import router from "./router";

// OneUI template components
import BaseBlock from "@/components/BaseBlock.vue";
import BaseBackground from "@/components/BaseBackground.vue";
import BasePageHeading from "@/components/BasePageHeading.vue";

// Shared admin components
import AppModal from "@/components/AppModal.vue";
import AppDataTable from "@/components/AppDataTable.vue";
import FormField from "@/components/FormField.vue";
import StatCard from "@/components/StatCard.vue";
import ToastHost from "@/components/ToastHost.vue";

// OneUI directives
import clickRipple from "@/directives/clickRipple";

// Auth store, for the global $can() permission helper below
import { useAuthStore } from "@/store/auth";

// Bootstrap JS (dropdowns, modals, offcanvas)
import * as bootstrap from "bootstrap";
window.bootstrap = bootstrap;

const app = createApp(App);

// Global components
app.component("BaseBlock", BaseBlock);
app.component("BaseBackground", BaseBackground);
app.component("BasePageHeading", BasePageHeading);
app.component("AppModal", AppModal);
app.component("AppDataTable", AppDataTable);
app.component("FormField", FormField);
app.component("StatCard", StatCard);

// Toasts are rendered by a single host mounted above the router view
app.component("ToastHost", ToastHost);

// Global directives
app.directive("click-ripple", clickRipple);

app.use(createPinia());
app.use(router);

// Global permission helper, mirrors the backend's permission codes:
//   v-if="$can('content.manage')"   — hides controls the API would 403
// Superusers pass every check.
app.config.globalProperties.$can = (code) => useAuthStore().hasPermission(code);

app.mount("#app");
