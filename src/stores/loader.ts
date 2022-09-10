import { defineStore } from "pinia";

export default defineStore("Loader", {
  state: () => ({
    loading: false,
    duration: 0,
    page: <HTMLHtmlElement | null>null,
  }),
  actions: {
    startLoading() {
      this.loading = true;
      this.duration = new Date().getTime();

      if (!this.page) {
        this.page = document.getElementsByTagName("html")[0] as HTMLHtmlElement;
      }

      this.page.classList.add("loading");
    },
    stopLoading() {
      const diff = new Date().getTime() - this.duration;
      const resetCursor = () => {
        this.page ? this.page.classList.remove("loading") : null;
      };

      if (diff <= 250) {
        setTimeout(() => {
          resetCursor();
          this.loading = false;
        }, 250 - diff);
      } else {
        resetCursor();
        this.loading = false;
      }
    },
  },
});
