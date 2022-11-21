import { defineStore } from "pinia";
import { ComputedRef } from "vue";

import { useFuse } from "@/utils";

import { FuseTrackOptions } from "@/composables/enums";
import { getPlaylist } from "@/composables/fetch/playlists";
import { Artist, FuseResult, Playlist, Track } from "@/interfaces";

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
     * @param id The id of the playlist to fetch
     */
    async fetchAll(id: string) {
      const playlist = await getPlaylist(id);

      this.info = playlist?.info || ({} as Playlist);
      this.allTracks = playlist?.tracks || [];
    },

    // async fetchArtists(id: string) {
    //   this.artists = await getPlaylistArtists(id);
    // },

    /**
     * Updates the playlist header info. This is used when the playlist is
     * updated.
     * @param info Playlist info
     */
    updatePInfo(info: Playlist) {
      const { duration, count } = this.info;

      this.info = info;

      this.info = { ...this.info, duration, count };
    },
    resetArtists() {
      this.artists = [];
    },
    resetQuery() {
      this.query = "";
    },
  },
  getters: {
    filteredTracks(): ComputedRef<FuseResult[]> {
      return useFuse(this.query, this.allTracks, FuseTrackOptions);
    },

    tracks(): Track[] {
      const tracks = this.filteredTracks.value.map((result: FuseResult) => {
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
