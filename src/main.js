import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";

import "../src/assets/css/global.scss";

import "animate.css";
import mitt from "mitt";

const emitter = mitt();

const app = createApp(App);
app.use(router);
app.provide('emitter', emitter);
app.mount('#app');