import { computed, ComputedRef, ref } from "vue";
import { useFuse } from "@vueuse/integrations/useFuse";
import { defineStore } from "pinia";

import { getPlaylist } from "../../composables/fetch/playlists";
import { Playlist, Track } from "../../interfaces";
import { Artist } from "./../../interfaces";

interface FussResult {
  item: string;
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
    resetQuery(){
      this.query = "";
    }
  },
  getters: {
    allHashes(): string[] {
      return this.allTracks.map((t) => {
        return t.hash;
      });
    },
    filteredHashes(): ComputedRef<FussResult[]> {
      const { results } = useFuse(this.query, this.allHashes, {
        matchAllWhenSearchEmpty: true,
      });
      return results as any;
    },

    tracks(): Track[] {
      const tracks = this.filteredHashes.value.map((result: FussResult) => {
        const t = {
          ...this.allTracks[result.refIndex],
          index: result.refIndex,
        };

        return t;
      });
      return tracks;
    },
  },
});
