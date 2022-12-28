import { useFuse } from "@/utils";
import { defineStore } from "pinia";
import { ComputedRef } from "vue";
import { AlbumDisc } from "./../../interfaces";

import { FuseTrackOptions } from "@/composables/enums";
import { maxAbumCards } from "@/stores/content-width";

import { getAlbum, getAlbumsFromArtist } from "../../composables/fetch/album";
import { Album, FuseResult, Track } from "../../interfaces";
import { useNotifStore } from "../notification";

interface Disc {
  [key: string]: Track[];
}

function sortByTrackNumber(tracks: Track[]) {
  return tracks.sort((a, b) => {
    if (a.track && b.track) {
      return a.track - b.track;
    }

    return 0;
  });
}

/**
 *
 * @param tracks The raw tracklist from the server
 * @returns A list of `Disc` objects
 */
function createDiscs(tracks: Track[]) {
  return tracks.reduce((group, track) => {
    const { disc } = track;

    group[disc] = group[disc] ?? [];
    group[disc].push(track);

    return group;
  }, {} as Disc);
}

export default defineStore("album", {
  state: () => ({
    query: "",
    info: <Album>{},
    srcTracks: <Track[]>[],
    albumArtists: <{ artisthash: string; albums: Album[] }[]>[],
    bio: null,
    discs: <Disc>{},
  }),
  actions: {
    /**
     * Fetches a single album information, artists and its tracks from the server
     * using the title and album-artist of the album.
     * @param hash title of the album
     */
    async fetchTracksAndArtists(hash: string) {
      const album = await getAlbum(hash, useNotifStore);

      this.srcTracks = album.tracks;
      this.info = album.info;

      const tracks = sortByTrackNumber(this.srcTracks);
      this.discs = createDiscs(tracks);

      this.srcTracks = Object.keys(this.discs).reduce(
        (tracks: Track[], disc) => {
          const disc_tracks = this.discs[disc];

          return [...tracks, ...disc_tracks];
        },
        []
      );

      this.srcTracks.forEach((t, index) => {
        t.master_index = index;
      });
    },
    async fetchArtistAlbums() {
      const albumartists = this.info.albumartists;

      const albumartisthashes = albumartists.map((artist) => artist.artisthash);

      this.albumArtists = await getAlbumsFromArtist(
        albumartisthashes.join(),
        maxAbumCards.value,
        this.info.albumhash
      );
    },
    resetQuery() {
      this.query = "";
    },
    resetAlbumArtists() {
      this.albumArtists = [];
    },
    makeFavorite() {
      this.info.is_favorite = true;
    },
    removeFavorite() {
      this.info.is_favorite = false;
    },
  },
  getters: {
    // discs(): Disc {
    //   return createDiscs(this.srcTracks);
    // },
    /**
     * All tracks ordered by disc and track number.
     */
    // allTracks(): Track[] {
    //   const tracks = Object.keys(this.discs).reduce((tracks: Track[], disc) => {
    //     const disc_tracks = this.discs[disc];

    //     return [...tracks, ...disc_tracks];
    //   }, []);

    //   tracks.map((t, index) => {
    //     t.master_index = index;
    //     return t;
    //   });

    //   return tracks;
    // },
    filteredTracks(): ComputedRef<FuseResult[]> {
      const discs = this.discs;
      let tracks: Track[] | AlbumDisc[] = [];

      Object.keys(discs).forEach((disc) => {
        const discHeader = {
          is_album_disc_number: true,
          album_page_disc_number: parseInt(disc),
        } as AlbumDisc;

        tracks = [...tracks, discHeader, ...discs[disc]];
      });

      return useFuse(this.query, tracks, FuseTrackOptions);
    },
    tracks(): Track[] {
      const tracks = this.filteredTracks.value.map((result: FuseResult) => {
        const t = {
          ...result.item,
          index: result.refIndex,
        };

        return t;
      });

      return tracks;
    },
  },
});

// TODO: Implement Disc interface using a class
