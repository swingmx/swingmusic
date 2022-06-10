import { playSources } from "@/composables/enums";
import { defineStore } from "pinia";

export default defineStore("navstore", {
  state: () => ({
    /**
     * Page header visibility status.
     */
    h_visible: false,
    title: {
      text: "",
      store: null,
      source: playSources,
    },
  }),
  actions: {
    /**
     * Toggles the store value of the page header visibility.
     *
     * @param {boolean} state The visibility state of the page header.
     */
    toggleShowPlay(state: boolean): void {
      this.h_visible = state;
    },
  },
});
