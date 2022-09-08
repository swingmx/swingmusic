import { computed, ComputedRef, ref } from "vue";
// import { useFuse } from "@vueuse/integrations/useFuse";
import { defineStore } from "pinia";

import { getPlaylist } from "../../composables/fetch/playlists";
import { Playlist, Track } from "../../interfaces";
import { Artist } from "./../../interfaces";
import { useFuse } from "@/utils";

interface FussResult {
  item: Track;
  refIndex: number;
}

export default defineStore("playlist-tracks", {
  state: () => ({
    info: <Playlist>{},
    query: "",
    allTracks: <Track[]>[],
    artists: <Artist[]>[],
  }),
  actions: {
    /**
     * Fetches a single playlist information, and its tracks from the server
     * @param playlistid The id of the playlist to fetch
     */
    async fetchAll(playlistid: string) {
      const playlist = await getPlaylist(playlistid);

      this.info = playlist?.info || ({} as Playlist);
      this.allTracks = playlist?.tracks || [];
    },

    // async fetchArtists(playlistid: string) {
    //   this.artists = await getPlaylistArtists(playlistid);
    // },
    /**
     * Updates the playlist header info. This is used when the playlist is
     * updated.
     * @param info Playlist info
     */
    updatePInfo(info: Playlist) {
      const duration = this.info.duration;
      this.info = info;
      this.info.duration = duration;
    },
    resetArtists() {
      this.artists = [];
    },
    resetQuery() {
      this.query = "";
    },
  },
  getters: {
    filteredTracks(): ComputedRef<FussResult[]> {
      return useFuse(this.query, this.allTracks, {
        keys: [
          { name: "title", weight: 1 },
          { name: "album", weight: 0.7 },
          { name: "artists", weight: 0.5 },
          { name: "albumartist", weight: 0.25 },
        ],
      });
    },

    tracks(): Track[] {
      const tracks = this.filteredTracks.value.map((result: FussResult) => {
        const t = {
          ...result.item,
          index: result.refIndex,
        };

        return t;
      });

      return tracks;
    },
  },
});
