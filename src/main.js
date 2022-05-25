import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import { createPinia } from "pinia";
import { MotionPlugin } from "@vueuse/motion";
import useCustomTransitions from "./transitions";
import "../src/assets/css/global.scss";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(MotionPlugin, useCustomTransitions);

app.mount("#app");
