import { useFuse } from "@/utils";
import { defineStore } from "pinia";
import { ComputedRef } from "vue";

import { FuseTrackOptions } from "@/composables/enums";

import { getAlbumTracks } from "../../composables/fetch/album";
import { AlbumInfo, Artist, FuseResult, Track } from "../../interfaces";
import { useNotifStore } from "../notification";

function sortTracks(tracks: Track[]) {
  return tracks.sort((a, b) => {
    if (a.track && b.track) {
      return a.track - b.track;
    }

    return 0;
  });
}

interface Discs {
  [key: string]: Track[];
}

function createDiscs(tracks: Track[]): Discs {
  return tracks.reduce((group, track) => {
    const { disc } = track;
    group[disc] = group[disc] ?? [];
    group[disc].push(track);
    return group;
  }, {} as Discs);
}

export default defineStore("album", {
  state: () => ({
    query: "",
    info: <AlbumInfo>{},
    allTracks: <Track[]>[],
    artists: <Artist[]>[],
    bio: null,
  }),
  actions: {
    /**
     * Fetches a single album information, artists and its tracks from the server
     * using the title and album-artist of the album.
     * @param hash title of the album
     */
    async fetchTracksAndArtists(hash: string) {
      this.allTracks = [];
      const album = await getAlbumTracks(hash, useNotifStore);

      const discs = createDiscs(sortTracks(album.tracks));
      Object.keys(discs).forEach((disc) => {
        this.allTracks.push(...discs[disc]);
      });

      this.info = album.info;
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
    discs(): Discs {
      return createDiscs(this.tracks);
    },
  },
});
