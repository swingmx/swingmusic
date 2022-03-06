import { defineStore } from "pinia";
import { ref } from "vue";

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
    changeTab(tab) {
      this.current = tab;
      console.log(this.current);
    },
  },
});
