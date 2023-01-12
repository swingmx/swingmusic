import { contextChildrenShowMode } from "@/composables/enums";
import { xxl } from "@/composables/useBreakpoints";
import { defineStore } from "pinia";

export default defineStore("settings", {
  state: () => ({
    use_np_img: true,
    use_sidebar: true,
    extend_width: false,
    contextChildrenShowMode: contextChildrenShowMode.click,
    artist_top_tracks_count: 5,
    repeat_all: true,
    repeat_one: false,
  }),
  actions: {
    toggleUseNPImg() {
      this.use_np_img = !this.use_np_img;
    },
    toggleDisableSidebar() {
      this.use_sidebar = !this.use_sidebar;
    },
    toggleExtendWidth() {
      this.extend_width = !this.extend_width;
    },
    setContextChildrenShowMode(mode: contextChildrenShowMode) {
      this.contextChildrenShowMode = mode;
    },
    toggleContextChildrenShowMode() {
      this.contextChildrenShowMode =
        this.contextChildrenShowMode === contextChildrenShowMode.click
          ? contextChildrenShowMode.hover
          : contextChildrenShowMode.click;
    },
    toggleRepeatMode() {
      if (this.repeat_all) {
        this.repeat_all = false;
        this.repeat_one = true;
        return;
      }

      if (this.repeat_one) {
        this.repeat_one = false;
        this.repeat_all = false;
        return;
      }

      if (!this.repeat_all && !this.repeat_one) {
        this.repeat_all = true;
      }
    },
  },
  getters: {
    can_extend_width(): boolean {
      return xxl.value;
    },
    no_repeat(): boolean {
      return !this.repeat_all && !this.repeat_one;
    },
  },
  persist: true,
});
