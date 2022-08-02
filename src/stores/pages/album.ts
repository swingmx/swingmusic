import { defineStore } from "pinia";
import { useNotifStore } from "../notification";
import { Track, Artist, AlbumInfo } from "../../interfaces";
import {
  getAlbumTracks,
  getAlbumArtists,
  getAlbumBio,
} from "../../composables/fetch/album";

function sortTracks(tracks: Track[]) {
  return tracks.sort((a, b) => {
    if (a.tracknumber && b.tracknumber) {
      return a.tracknumber - b.tracknumber;
    }

    return 0;
  });
}

interface Discs {
  [key: string]: Track[];
}

function createDiscs(tracks: Track[]): Discs {
  return tracks.reduce((group, track) => {
    const { discnumber } = track;
    group[discnumber] = group[discnumber] ?? [];
    group[discnumber].push(track);
    return group;
  }, {} as Discs);
}

export default defineStore("album", {
  state: () => ({
    info: <AlbumInfo>{},
    tracks: <Track[]>[],
    discs: <Discs>{},
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
      this.tracks = [];
      const album = await getAlbumTracks(hash, useNotifStore);
      const artists = await getAlbumArtists(hash);

      this.discs = createDiscs(sortTracks(album.tracks));
      Object.keys(this.discs).forEach((disc) => {
        this.tracks.push(...this.discs[disc]);
      });

      this.info = album.info;
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
