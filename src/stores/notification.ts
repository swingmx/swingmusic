import { defineStore } from "pinia";
import { Notif } from "../interfaces";
import { NotifType } from "../composables/enums";

const useNotifStore = defineStore("notification", {
  state: () => ({
    notifs: <Notif[]>[],
  }),
  actions: {
    showNotification(new_text: string, new_type?: NotifType) {
      this.notifs.push(<Notif>{
        text: new_text,
        type: new_type,
      });

      setTimeout(() => {
        this.notifs.shift();
      }, 3000);
    },
  },
});

class Notification {
  constructor(text: string, type: NotifType = NotifType.Info) {
    useNotifStore().showNotification(text, type);
  }
}

export { useNotifStore, Notification, NotifType };
