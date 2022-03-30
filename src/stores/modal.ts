import { defineStore } from "pinia";
import { Track } from "../interfaces";
enum ModalOptions {
  newPlaylist,
  editPlaylist,
}

export default defineStore("newModal", {
  state: () => ({
    title: "",
    options: ModalOptions,
    component: "",
    props: {},
    visible: false,
  }),
  actions: {
    showModal(modalOption: string) {
      this.component = modalOption;
      this.visible = true;
    },
    showNewPlaylistModal(track: Track) {
      this.component = ModalOptions.newPlaylist;
      this.props.track = track;
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
