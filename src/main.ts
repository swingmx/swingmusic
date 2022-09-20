import "./assets/scss/index.scss";

import { createApp } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";


import App from "./App.vue";
import router from "./router";
import vTooltip from "./directives/vTooltip";

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

app.use(pinia);
app.use(router);
app.directive("tooltip", vTooltip);

app.mount("#app")
