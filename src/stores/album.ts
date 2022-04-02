import { defineStore } from "pinia";
import { Track, Artist, AlbumInfo } from "../interfaces";
import {
  getAlbumTracks,
  getAlbumArtists,
  getAlbumBio,
} from "../composables/album";

export default defineStore("album", {
  state: () => ({
    info: <AlbumInfo>{},
    tracks: <Track[]>[],
    artists: <Artist[]>[],
    bio: null,
  }),
  actions: {
    async fetchTracksAndArtists(title: string, albumartist: string) {
      const tracks = await getAlbumTracks(title, albumartist);
      const artists = await getAlbumArtists(title, albumartist);

      this.tracks = tracks.tracks;
      this.info = tracks.info;
      this.artists = artists;
    },
    fetchBio(title: string, albumartist: string) {
      getAlbumBio(title, albumartist).then((bio) => {
        this.bio = bio;
      });
    },
  },
});
