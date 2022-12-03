import { useFuse } from "@/utils";
import { defineStore } from "pinia";
import { ComputedRef } from "vue";
import { AlbumDisc } from "./../../interfaces";

import { FuseTrackOptions } from "@/composables/enums";
import { content_width } from "@/stores/content-width";

import {
    getAlbumsFromArtist,
    getAlbumTracks
} from "../../composables/fetch/album";
import { Album, Artist, FuseResult, Track } from "../../interfaces";
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

function albumHasNoDiscs(album: Album) {
  if (album.is_single) return true;

  return false;
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
    rawTracks: <Track[]>[],
    artists: <Artist[]>[],
    albumArtists: <{ artist: string; albums: Album[] }[]>[],
    bio: null,
  }),
  actions: {
    /**
     * Fetches a single album information, artists and its tracks from the server
     * using the title and album-artist of the album.
     * @param hash title of the album
     */
    async fetchTracksAndArtists(hash: string) {
      const album = await getAlbumTracks(hash, useNotifStore);
      this.rawTracks = album.tracks;
      this.info = album.info;
    },
    async fetchArtistAlbums() {
      const albumartists = this.info.albumartists;
      const cardWidth = 10 * 16;
      const visible_cards = Math.floor(content_width.value / cardWidth);
      const albumartisthashes = albumartists.map((artist) => artist.hash);

      this.albumArtists = await getAlbumsFromArtist(
        albumartisthashes.join(),
        visible_cards,
        this.info.albumhash
      );
    },
    resetQuery() {
      this.query = "";
    },
    resetAlbumArtists() {
      this.albumArtists = [];
    },
  },
  getters: {
    discs(): Disc {
      return createDiscs(sortByTrackNumber(this.rawTracks));
    },
    allTracks(): Track[] {
      return Object.keys(this.discs).reduce((tracks: Track[], disc) => {
        const disc_tracks = this.discs[disc];

        return [...tracks, ...disc_tracks];
      }, []);
    },
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
