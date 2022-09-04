import "./assets/scss/index.scss";

import { createPinia } from "pinia";
import { createApp } from "vue";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import vTooltip from "./directives/vTooltip";

import App from "./App.vue";
import router from "./router";

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

app.use(pinia);
app.use(router);
app.directive("tooltip", vTooltip);

app.mount("#app");
