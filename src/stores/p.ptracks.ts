import { defineStore } from "pinia";
import { getPlaylist } from "../composables/playlists";
import { Track, Playlist } from "../interfaces";

export default defineStore("playlist-tracks", {
  state: () => ({
    info: <Playlist>{},
    tracks: <Track[]>[],
  }),
  actions: {
    async fetchAll(playlistid: string) {
      const playlist = await getPlaylist(playlistid);
      this.info = playlist.info;
      this.tracks = playlist.tracks;
    },
    updatePInfo(info: Playlist) {
      this.info = info;
    },
  },
});
