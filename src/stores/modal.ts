import { defineStore } from "pinia";
import { Playlist, Track } from "../interfaces";

enum ModalOptions {
  newPlaylist = "newPlaylist",
  updatePlaylist = "editPlaylist",
}

export default defineStore("newModal", {
  state: () => ({
    title: "",
    options: ModalOptions,
    component: "",
    props: <any>{},
    visible: false,
  }),
  actions: {
    showModal(modalOption: string) {
      this.component = modalOption;
      this.visible = true;
    },
    showNewPlaylistModal(track?: Track) {
      this.component = ModalOptions.newPlaylist;

      if (track) {
        this.props.track = track;
      }
      
      this.visible = true;
    },
    showEditPlaylistModal(playlist: Playlist) {
      this.component = ModalOptions.updatePlaylist;
      this.props = playlist;
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
