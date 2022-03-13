import { defineStore } from "pinia";
import normalize from "../composables/normalizeContextMenu";

export default defineStore("context-menu", {
  state: () => ({
    visible: false,
    x: 0,
    y: 0,
  }),
  actions: {
    showContextMenu(e) {
      this.visible = true;
      const yo = normalize(e.clientX, e.clientY);
      this.x = yo.normalizedX;
      this.y = yo.normalizedY;
      console.log(yo);
    },
    hideContextMenu() {
      this.visible = false;
    },
  },
});
