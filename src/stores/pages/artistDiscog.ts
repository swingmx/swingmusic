import { defineStore } from "pinia";
import { discographyAlbumTypes } from "@/composables/enums";
import { Album } from "@/interfaces";
import { getArtistAlbums } from "@/composables/fetch/artists";

export default defineStore("artistDiscography", {
  state: () => ({
    artistname: <string>"",
    page: discographyAlbumTypes.all,

    toShow: <Album[]>[],

    albums: <Album[]>[],
    eps: <Album[]>[],
    singles: <Album[]>[],
    appearances: <Album[]>[],
  }),
  actions: {
    setAlbums(page: discographyAlbumTypes) {
      this.setPage(page);
      switch (page) {
        case discographyAlbumTypes.albums:
          this.toShow = this.albums;
          break;
        case discographyAlbumTypes.eps:
          this.toShow = this.eps;
          break;
        case discographyAlbumTypes.singles:
          this.toShow = this.singles;
          break;
        case discographyAlbumTypes.appearances:
          this.toShow = this.appearances;
          break;
        default:
          this.toShow = this.albums.concat(
            this.eps,
            this.singles,
            this.appearances
          );
      }
    },
    setPage(page: discographyAlbumTypes | undefined) {
      // @ts-ignore
      this.page = page;
    },
    fetchAlbums(artisthash: string) {
      getArtistAlbums(artisthash, 0, true)
        .then((data) => {
          this.albums = data.albums;
          this.eps = data.eps;
          this.singles = data.singles;
          this.appearances = data.appearances;
          this.artistname = data.artistname;
        })
        .then(() => this.setAlbums(this.page));
    },
    resetAlbums() {
      this.albums = [];
      this.eps = [];
      this.singles = [];
      this.appearances = [];

      this.toShow = [];
      this.artistname = "";
    },
  },
});
