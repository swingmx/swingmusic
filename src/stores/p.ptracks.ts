import { defineStore } from "pinia";
import { getPlaylist, getPTracks } from "../composables/playlists";
import { Track, Playlist } from "../interfaces";

export default defineStore("playlist-tracks", {
  state: () => ({
    playlist: <Playlist>{},
  }),
  actions: {
    async fetchAll(playlistid: string) {
      const playlist = await getPlaylist(playlistid);
      this.playlist = playlist;
    },
  },
});
