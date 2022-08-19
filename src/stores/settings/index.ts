import { defineStore } from "pinia";
import useQueueStore from "../queue";

export default defineStore("settings", {
  state: () => ({
    use_side_np: false,
    use_right_np: true,
  }),
  actions: {
    toggleNPs() {
      this.use_side_np = !this.use_side_np;
      this.use_right_np = !this.use_right_np;
      useQueueStore().bindProgressElem();
    },
    toggleUseSideNP() {
      this.toggleNPs();
    },
    toggleUseRightNP() {
      this.toggleNPs();
    },
  },
  getters: {},
  persist: true,
});
