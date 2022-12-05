import { defineStore } from "pinia";

import { Artist, Album, Track } from "@/interfaces";
import { getArtistData, getArtistAlbums } from "@/composables/fetch/artists";
import { maxAbumCards } from "@/stores/content-width";

export default defineStore("artistPage", {
  state: () => ({
    info: <Artist>{},
    albums: <Album[]>[],
    tracks: <Track[]>[],
  }),
  actions: {
    async getData(hash: string) {
      const { artist, tracks } = await getArtistData(hash);

      this.info = artist;
      this.tracks = tracks;
    },
    async getArtistAlbums() {
      const albums = await getArtistAlbums(
        this.info.artisthash,
        maxAbumCards.value
      );

      if (albums.length > 0) {
        this.albums = albums;
      }
    },
    resetAlbums() {
      this.albums = [];
    },
  },
});
