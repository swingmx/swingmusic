import { defineStore } from "pinia";
import normalize from "../composables/normalizeContextMenu";
import { Option } from "../interfaces";
import { ContextSrc } from "../composables/enums";

function getPlaceholders(length: number) {
  let list: Option[] = [];

  for (let index = 0; index < length; index++) {
    list.push("" as Option);
  }

  return list;
}

getPlaceholders(5);

export default defineStore("context-menu", {
  state: () => ({
    visible: false,
    options: getPlaceholders(5),
    x: 500,
    y: 500,
    normalizedX: false,
    normalizedY: false,
    src: <null | string>"",
  }),
  actions: {
    showContextMenu(
      e: any,
      context_options: Promise<Option[]>,
      src: ContextSrc
    ) {
      if (this.visible) {
        this.visible = false;
        return;
      }

      this.visible = true;
      context_options.then((options) => {
        this.options = options;
      });

      const xy = normalize(e.clientX, e.clientY);

      this.x = xy.normalX;
      this.y = xy.normalY;

      this.normalizedX = xy.normalizedX;
      this.normalizedY = xy.normalizedY;
      this.src = src;
    },
    hideContextMenu() {
      this.visible = false;
      this.src = null;
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
