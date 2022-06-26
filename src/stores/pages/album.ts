import { defineStore } from "pinia";
import { useNotifStore } from "../notification";
import { Track, Artist, AlbumInfo } from "../../interfaces";
import {
  getAlbumTracks,
  getAlbumArtists,
  getAlbumBio,
} from "../../composables/pages/album";

function sortTracks(tracks: Track[]) {
  return tracks.sort((a, b) => {
    if (a.tracknumber && b.tracknumber) {
      return a.tracknumber - b.tracknumber;
    }

    return 0;
  });
}

export default defineStore("album", {
  state: () => ({
    info: <AlbumInfo>{},
    tracks: <Track[]>[],
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
      const tracks = await getAlbumTracks(hash, useNotifStore);
      const artists = await getAlbumArtists(hash);

      this.tracks = sortTracks(tracks.tracks);
      this.info = tracks.info;
      this.artists = artists;
    },
    /**
     * Fetches the album bio from the server
     * @param {string} hash title of the album
     */
    fetchBio(hash: string) {
      this.bio = null;
      getAlbumBio(hash).then((bio) => {
        this.bio = bio;
      });
    },
  },
});
