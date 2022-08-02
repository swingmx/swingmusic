import { Artist } from "./../../interfaces";
import { defineStore } from "pinia";
import {
  getPlaylist,
  getPlaylistArtists,
} from "../../composables/fetch/playlists";
import { Track, Playlist } from "../../interfaces";

export default defineStore("playlist-tracks", {
  state: () => ({
    info: <Playlist>{},
    tracks: <Track[]>[],
    artists: <Artist[]>[],
  }),
  actions: {
    /**
     * Fetches a single playlist information, and its tracks from the server
     * @param playlistid The id of the playlist to fetch
     */
    async fetchAll(playlistid: string) {
      const playlist = await getPlaylist(playlistid);

      this.info = playlist.info;
      this.tracks = playlist.tracks;
    },

    async fetchArtists(playlistid: string) {
      this.artists = await getPlaylistArtists(playlistid);
    },
    /**
     * Updates the playlist header info. This is used when the playlist is
     * updated.
     * @param info Playlist info
     */
    updatePInfo(info: Playlist) {
      this.info = info;
    },
  },
});
