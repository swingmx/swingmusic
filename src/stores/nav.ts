import { defineStore } from "pinia";

export default defineStore("navmanagement", {
  state: () => ({
    showPlay: false,
  }),
  actions: {
    toggleShowPlay(state: boolean) {
      this.showPlay = state;
    },
  },
});
