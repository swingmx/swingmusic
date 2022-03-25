import { defineStore } from "pinia";

enum ModalOptions {
  newPlaylist = "newPlaylist",
  editPlaylist = "editPlaylist",
}

export default defineStore("newModal", {
  state: () => ({
    title: "",
    options: ModalOptions,
    component: "",
    visible: false,
  }),
  actions: {
    showModal(modalOption: string) {
      this.component = modalOption;
      this.visible = true;
    },
    hideModal() {
      this.visible = false;
    },
    setTitle(new_title: string) {
      this.title = new_title;
    },
  },
});
