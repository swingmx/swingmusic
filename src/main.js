import "./registerServiceWorker";
import "../src/assets/css/global.scss";

import { MotionPlugin } from "@vueuse/motion";
import { createPinia } from "pinia";
import { createApp } from "vue";

import App from "./App.vue";
import router from "./router";
import useCustomTransitions from "./transitions";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(MotionPlugin, useCustomTransitions);

app.mount("#app");
