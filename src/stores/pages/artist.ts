import { defineStore } from "pinia";

import { Artist, Album, Track } from "@/interfaces";
import { getArtistData } from "@/composables/fetch/artists";

export default defineStore("artistPage", {
  state: () => ({
    info: <Artist>{},
    albums: <Album[]>[],
    tracks: <Track[]>[],
  }),
  actions: {
    async getData(hash: string) {
      const { artist, albums, tracks } = await getArtistData(hash);

      this.info = artist;
      this.tracks = tracks;
      this.albums = albums;
    },
  },
});
