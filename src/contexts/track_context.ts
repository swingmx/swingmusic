import { Artist, Playlist, Track } from "../interfaces";

// @ts-ignore
import { Option } from "../interfaces";
import Router from "../router";

import {
  addTrackToPlaylist,
  getAllPlaylists,
} from "../composables/fetch/playlists";

import useModalStore from "../stores/modal";
import useQueueStore from "../stores/queue";
import { Routes } from "@/router/routes";
/**
 * Returns a list of context menu items for a track.
 * @param  {any} track a track object.
 * @param {any} modalStore a pinia store.
 * @return {Array<Option>()} a list of context menu items.
 */

export default async (
  track: Track,
  modalStore: typeof useModalStore,
  QueueStore: typeof useQueueStore
): Promise<Option[]> => {
  const separator: Option = {
    type: "separator",
  };

  const single_artist = track.artist.length === 1;
  const single_album_artist = track.albumartist.length === 1;

  const goToArtist = (artists: Artist[]) => {
    if (artists.length === 1) {
      return false;
    }

    return artists.map((artist) => {
      return <Option>{
        label: artist.name,
        action: () =>
          Router.push({
            name: Routes.artist,
            params: {
              hash: artist.artisthash,
            },
          }),
      };
    });
  };

  async function addToPlaylist() {
    const new_playlist = <Option>{
      label: "New playlist",
      action: () => {
        modalStore().showNewPlaylistModal(track);
      },
    };

    let playlists = <Option[]>[];
    const p = await getAllPlaylists();

    playlists = p.map((playlist: Playlist) => {
      return <Option>{
        label: playlist.name,
        action: () => {
          addTrackToPlaylist(playlist, track);
        },
      };
    });

    return [new_playlist, separator, ...playlists];
  }

  const add_to_playlist: Option = {
    label: "Add to Playlist",
    children: await addToPlaylist(),
    icon: "plus",
  };

  const add_to_q: Option = {
    label: "Add to Queue",
    action: () => {
      QueueStore().addTrackToQueue(track);
    },
    icon: "add_to_queue",
  };

  const play_next: Option = {
    label: "Play next",
    action: () => {
      QueueStore().playTrackNext(track);
    },
    icon: "play_next",
  };

  const go_to_folder: Option = {
    label: "Go to Folder",
    action: () => {
      Router.push({
        name: Routes.folder,
        params: { path: track.folder },
      });
    },
    icon: "folder",
  };

  const go_to_artist: Option = {
    label: `Go to Artist`,
    icon: "artist",
    action: () => {
      single_artist
        ? Router.push({
            name: Routes.artist,
            params: {
              hash: track.artist[0].artisthash,
            },
          })
        : null;
    },
    children: goToArtist(track.artist),
  };

  const go_to_alb_artist: Option = {
    label: `Go to Album Artist`,
    action: () => {
      single_album_artist
        ? Router.push({
            name: Routes.artist,
            params: {
              hash: track.albumartist[0].artisthash,
            },
          })
        : null;
    },
    icon: "artist",
    children: goToArtist(track.albumartist),
  };

  const go_to_album: Option = {
    label: "Go to Album",
    action: () => {
      Router.push({
        name: Routes.album,
        params: { hash: track.albumhash },
      });
    },
    icon: "album",
  };

  const del_track: Option = {
    label: "Delete Track",
    action: () => console.log("Delete Track"),
    icon: "delete",
    critical: true,
  };

  const add_to_fav: Option = {
    label: "I love this",
    action: () => console.log("I love this"),
    icon: "heart",
  };

  const options: Option[] = [
    play_next,
    add_to_q,
    separator,
    add_to_playlist,
    separator,
    go_to_album,
    go_to_folder,
    separator,
    go_to_artist,
    go_to_alb_artist,
    // add_to_fav,
    // separator,
    // del_track,
  ];

  return options;
};

// TODO: Find a way to fetch playlists lazily. ie. When the "Add to playlist" option is triggered.
