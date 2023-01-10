import { defineStore } from "pinia";
import { Playlist, Track } from "../interfaces";

enum ModalOptions {
  newPlaylist,
  updatePlaylist,
  welcome,
  deletePlaylist,
}

export default defineStore("newModal", {
  state: () => ({
    title: "",
    options: ModalOptions,
    component: <any>null,
    props: <any>{},
    visible: false,
  }),
  actions: {
    showModal(modalOption: ModalOptions) {
      this.component = modalOption;
      this.visible = true;
    },
    showNewPlaylistModal(track?: Track) {
      if (track) {
        this.props.track = track;
      }
      this.showModal(ModalOptions.newPlaylist);
    },
    showEditPlaylistModal(playlist: Playlist) {
      this.props = playlist;
      this.showModal(ModalOptions.updatePlaylist);
    },
    showWelcomeModal() {
      this.showModal(ModalOptions.welcome);
    },
    showDeletePlaylistModal(pid: number) {
      this.props = {
        pid: pid,
      };
      this.showModal(ModalOptions.deletePlaylist);
    },
    hideModal() {
      this.visible = false;
      this.setTitle("");
    },
    setTitle(new_title: string) {
      this.title = new_title;
    },
  },
});
