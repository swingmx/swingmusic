import { defineStore } from "pinia";
import useQueueStore from "../queue";

export default defineStore("settings", {
  state: () => ({
    use_alt_np: false,
  }),
  actions: {
    toggleUseRightNP() {
      this.use_alt_np = !this.use_alt_np;
      useQueueStore();
    },
  },
  getters: {},
  persist: true,
});
