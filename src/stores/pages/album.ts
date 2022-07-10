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
    bio: "HELLBOY is the fourth & final mixtape by Lil Peep, released on September 25, 2016. The mixtape caught people’s attention, pushing him into the mainstream light. The title HELLBOY is a reference to the animated movie Hellboy Animated: Blood and Iron, as Peep explains in a GQ interview. This album’s title was explained by Smokeasac, who produced many songs on this album: 'I remember when we made “Hellboy”. He explained to me why he chose the name. He explained that it was because he knew that “Hellboy” came off as intimidating and scary to some but it was because he ",
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
