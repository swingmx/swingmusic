import { defineStore } from "pinia";
import perks from "../composables/perks";

const tablist = {
  home: "home",
  search: "search",
  queue: "queue",
};

export default defineStore("tabs", {
  state: () => ({
    tabs: tablist,
    current: tablist.home,
  }),
  actions: {
    changeTab(tab: string) {
      if (tab === this.tabs.queue) {
        setTimeout(() => {
          perks.focusCurrent();
        }, 500);
      }
      this.current = tab;
    },
    switchToQueue() {
      this.changeTab(tablist.queue);
    },
    switchToSearch() {
      this.changeTab(tablist.search);
    },
    switchToHome() {
      this.changeTab(tablist.home);
    },
  },
});
