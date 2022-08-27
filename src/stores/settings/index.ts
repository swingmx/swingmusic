import { defineStore } from "pinia";

export default defineStore("settings", {
  state: () => ({
    use_alt_np: false,
    use_sidebar: true,
  }),
  actions: {
    toggleUseRightNP() {
      if (!this.use_sidebar) return;
      this.use_alt_np = !this.use_alt_np;
    },
    toggleDisableSidebar() {
      this.use_sidebar = !this.use_sidebar;
    },
  },
  getters: {
    show_alt_np(): boolean {
      return this.use_sidebar && this.use_alt_np;
    },
    show_default_np(): boolean {
      return !this.show_alt_np;
    },
    disable_show_alt_np(): boolean {
      return !this.use_sidebar;
    },
  },
  persist: true,
});
