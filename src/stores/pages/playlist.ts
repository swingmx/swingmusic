import { ComputedRef } from "vue";
import { defineStore } from "pinia";

import { useFuse } from "@/utils";

import { FuseTrackOptions } from "@/composables/enums";
import { getPlaylist } from "@/composables/fetch/playlists";
import { FussResult, Artist, Playlist, Track } from "@/interfaces";

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
      return useFuse(this.query, this.allTracks, FuseTrackOptions);
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
