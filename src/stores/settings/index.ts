import { xxl, xl } from "@/composables/useBreakpoints";
import { defineStore } from "pinia";

export default defineStore("settings", {
  state: () => ({
    use_alt_np: false,
    use_sidebar: true,
    extend_width: false,
  }),
  actions: {
    toggleUseRightNP() {
      if (!this.use_sidebar) return;
      this.use_alt_np = !this.use_alt_np;
    },
    toggleDisableSidebar() {
      this.use_sidebar = !this.use_sidebar;
    },
    toggleExtendWidth() {
      this.extend_width = !this.extend_width;
    },
  },
  getters: {
    show_alt_np(): boolean {
      return xl.value && this.use_sidebar && this.use_alt_np;
    },
    show_default_np(): boolean {
      return !this.show_alt_np;
    },
    disable_show_alt_np(): boolean {
      return !xl.value || !this.use_sidebar;
    },
    hide_queue_page(): boolean {
      return this.use_sidebar;
    },
    extend_width_enabled(): boolean {
     return xxl.value
    },
  },
  persist: true,
});
