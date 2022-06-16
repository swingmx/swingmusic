import { defineStore } from "pinia";
import { Track, Artist, AlbumInfo } from "../../interfaces";
import {
  getAlbumTracks,
  getAlbumArtists,
  getAlbumBio,
} from "../../composables/fetch/album";

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
     * @param title title of the album
     * @param albumartist artist of the album
     */
    async fetchTracksAndArtists(title: string, albumartist: string) {

      const tracks = await getAlbumTracks(title, albumartist);
      const artists = await getAlbumArtists(title, albumartist);

      this.tracks = tracks.tracks;
      this.info = tracks.info;
      this.artists = artists;
    },
    /**
     * Fetches the album bio from the server
     * @param title title of the album
     * @param albumartist artist of the album
     */
    fetchBio(title: string, albumartist: string) {
      this.bio = null;
      getAlbumBio(title, albumartist).then((bio) => {
        this.bio = bio;
      });
    },
  },
});
