import { defineStore } from "pinia";

export default defineStore("navmanagement", {
  state: () => ({
    showPlay: true,
  }),
  actions: {
    toggleShowPlay() {
      this.showPlay = !this.showPlay;
      console.log(this.showPlay);
    },
  },
});
