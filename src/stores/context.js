import { defineStore } from "pinia";
import normalize from "../composables/normalizeContextMenu";

export default defineStore("context-menu", {
  state: () => ({
    visible: false,
    options: [],
    x: 0,
    y: 0,
  }),
  actions: {
    showContextMenu(e, context_options) {
      if (this.visible) {
        this.visible = false;
        return
      }

      this.options = context_options;
      const yo = normalize(e.clientX, e.clientY);
      this.x = yo.normalizedX;
      this.y = yo.normalizedY;
      this.visible = true;
    },
    hideContextMenu() {
      this.visible = false;
    },
  },
});
