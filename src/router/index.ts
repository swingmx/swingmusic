import { routes } from "./routes";
import { createRouter, createWebHashHistory, RouterOptions } from "vue-router";

const router = createRouter({
  mode: "hash",
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
} as RouterOptions);

export default router;
