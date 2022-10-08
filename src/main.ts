import { createApp } from "vue";
import { createPinia } from "pinia";

import {
    RecycleScroller,
    DynamicScroller,
    DynamicScrollerItem,
    // @ts-ignore
} from "vue-virtual-scroller";

import { autoAnimatePlugin } from "@formkit/auto-animate/vue";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

import "./assets/scss/index.scss";
import "vue-virtual-scroller/dist/vue-virtual-scroller.css";

import App from "./App.vue";
import router from "./router";
import vTooltip from "./directives/vTooltip";

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

app.use(pinia);
app.use(router);
app.directive("tooltip", vTooltip);
app.use(autoAnimatePlugin);
app.component("RecycleScroller", RecycleScroller);
app.component("DynamicScroller", DynamicScroller);
app.component("DynamicScrollerItem", DynamicScrollerItem);

app.mount("#app");
