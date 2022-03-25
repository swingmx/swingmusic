import { defineStore } from "pinia";

const useNotificationStore = defineStore("notification", {
  state: () => ({
    text: "",
    visible: false,
  }),
  actions: {
    showNotification(new_text: string) {
      this.text = new_text;
      this.visible = true;

      setTimeout(() => {
        this.visible = false;
      }, 2000);
    },
  },
});

class Notification {
  constructor(text: string) {
    useNotificationStore().showNotification(text);
  }
}

export { useNotificationStore, Notification };
