import { defineStore } from "pinia";
import normalizeContextMenu from "../composables/normalizeContextMenu";

export default defineStore("context-menu", {
  state: () => ({
    visible: false,
    x: 0,
    y: 0,
  }),
  actions: {
    showContextMenu(e) {
      this.visible = true;
      const { normalX, normalY } = normalizeContextMenu(e.clientX, e.clientY);
      this.x = normalX;
      this.y = normalY;
    },
    hideContextMenu() {
      this.visible = false;
    },
  },
});
