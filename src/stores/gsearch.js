import { defineStore } from "pinia";
import useDebouncedRef from "../composables/useDebouncedRef";

export default defineStore("gsearch", {
  state: () => ({
    filters: [],
    query: useDebouncedRef("", 600),
    results: {
      tracks: {
        items: [],
        more: false,
      },
      albums: {
        items: [],
        more: false,
      },
      artists: {
        items: [],
        more: false,
      },
    },
  }),
  actions: {
    addFilter(filter) {
      if (this.filters.includes(filter)) {
        return;
      }
      this.filters.push(filter);
    },
    removeFilter(filter) {
      this.filters = this.filters.filter((f) => f !== filter);
    },
    removeLastFilter() {
      this.filters.pop();
    },
    updateQuery(query) {
      this.query = query;
    },
    updateTrackResults(results) {
      this.results.tracks = results;
    },
    addMoreTrackResults(results) {
      this.results.tracks.items = [
        ...this.results.tracks.items,
        ...results.items,
      ];
    },
    updateAlbumResults(results) {
      this.results.albums = results;
    },
    addMoreAlbumResults(results) {
      this.results.albums.items = [
        ...this.results.albums.items,
        ...results.items,
      ];
    },
    updateArtistResults(results) {
      this.results.artists = results;
    },
    addMoreArtistResults(results) {
      this.results.artists.items = [
        ...this.results.artists.items,
        ...results.items,
      ];
    },
  },
});
