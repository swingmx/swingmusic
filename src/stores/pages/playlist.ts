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
    bannerPos: 0,
    allTracks: <Track[]>[],
    artists: <Artist[]>[],
  }),
  actions: {
    /**
     * Fetches a single playlist information, and its tracks from the server
     * @param id The id of the playlist to fetch
     */
    async fetchAll(id: string) {
      this.resetBannerPos();
      const playlist = await getPlaylist(id);

      this.info = playlist?.info || ({} as Playlist);
      this.bannerPos = this.info.banner_pos;
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
      this.bannerPos = this.info.banner_pos;
    },
    plusBannerPos() {
      this.bannerPos !== 100 ? (this.bannerPos += 10) : null;
    },
    minusBannerPos() {
      this.bannerPos !== 0 ? (this.bannerPos -= 10) : null;
    },
    resetArtists() {
      this.artists = [];
    },
    resetQuery() {
      this.query = "";
    },
    resetBannerPos() {
      this.bannerPos = 50;
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
    bannerPosUpdated(): boolean {
      return this.info.banner_pos - this.bannerPos !== 0;
    },
  },
});
