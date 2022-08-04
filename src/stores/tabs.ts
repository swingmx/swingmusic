import { defineStore } from "pinia";
import { focusElem } from "@/utils";

const tablist = {
  home: "home",
  queue: "queue",
  search: "search",
};

export default defineStore("tabs", {
  state: () => ({
    tabs: tablist,
    current: tablist.queue,
  }),
  actions: {
    changeTab(tab: string) {
      if (tab === this.tabs.queue) {
        setTimeout(() => {
          focusElem("currentInQueue");
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
