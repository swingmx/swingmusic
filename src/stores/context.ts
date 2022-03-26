import { defineStore } from "pinia";
import normalize from "../composables/normalizeContextMenu";
import { Option } from "../interfaces";

export default defineStore("context-menu", {
  state: () => ({
    visible: false,
    options: Array<Option>(),
    x: 500,
    y: 500,
    normalizedX: false,
    normalizedY: false,
  }),
  actions: {
    showContextMenu(e: any, context_options: Promise<Option[]>) {
      if (this.visible) {
        this.visible = false;
        return;
      }

      context_options.then((options) => {
        this.options = options;
      });

      const yo = normalize(e.clientX, e.clientY);

      this.x = yo.normalX;
      this.y = yo.normalY;

      this.normalizedX = yo.normalizedX;
      this.normalizedY = yo.normalizedY;

      this.visible = true;
    },
    hideContextMenu() {
      this.visible = false;
    },
    hasManyChildren() {
      let result = false;

      this.options.forEach((option: Option) => {
        if (option.children && option.children.length > 9) {
          result = true;
        }
      });

      return result;
    },
  },
});
