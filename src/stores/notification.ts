import { defineStore } from "pinia";

enum NotificationType {
  Success,
  Error,
}

const useNotificationStore = defineStore("notification", {
  state: () => ({
    text: "",
    type: NotificationType.Success,
    visible: false,
  }),
  actions: {
    showNotification(new_text: string, new_type?: NotificationType) {
      console.log(arguments);
      this.text = new_text;
      this.type = new_type;
      this.visible = true;

      setTimeout(() => {
        this.visible = false;
      }, 2000);
    },
  },
});

class Notification {
  constructor(text: string, type?: NotificationType) {
    useNotificationStore().showNotification(text, type);
  }
}

export { useNotificationStore, Notification, NotificationType };
