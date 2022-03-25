import { defineStore } from "pinia";
import { Playlist } from "../interfaces";
import { getAllPlaylists } from "../composables/playlists";

export default defineStore("playlists", {
  state: () => ({
    playlists: <Playlist[]>[],
  }),
  actions: {
    fetchAll() {
      
    },
  },
});
