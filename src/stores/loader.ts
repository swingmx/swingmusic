import { defineStore } from "pinia";

export default defineStore("Loader", {
  state: () => ({
    loading: false,
    duration: 0,
  }),
  actions: {
    startLoading() {
      this.loading = true;
      this.duration = new Date().getTime();
    },
    stopLoading() {
      const diff = new Date().getTime() - this.duration;

      if (diff <= 250) {
        setTimeout(() => {
          this.loading = false;
        }, 250 - diff);
      } else {
        this.loading = false;
      }
    },
  },
});
