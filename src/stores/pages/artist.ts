import { defineStore } from "pinia";

import { Artist, Album, Track } from "@/interfaces";
import { getArtistData, getArtistAlbums } from "@/composables/fetch/artists";
import { maxAbumCards } from "@/stores/content-width";

export default defineStore("artistPage", {
  state: () => ({
    info: <Artist>{},
    tracks: <Track[]>[],
    albums: <Album[]>[],
    eps: <Album[]>[],
    singles: <Album[]>[],
  }),
  actions: {
    async getData(hash: string) {
      const { artist, tracks } = await getArtistData(hash);

      this.info = artist;
      this.tracks = tracks;
    },
    async getArtistAlbums() {
      const { albums, eps, singles } = await getArtistAlbums(
        this.info.artisthash,
        maxAbumCards.value
      );

      this.albums = albums;
      this.eps = eps;
      this.singles = singles;

      // if (albums.length > 0) {
      // }

      // if (eps.length > 0) {
      // }

      // if (singles.length > 0) {
      // }
    },
    resetAlbums() {
      this.albums = [];
      this.eps = [];
      this.singles = [];
    },
  },
});
