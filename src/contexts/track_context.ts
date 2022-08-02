import { Playlist, Track } from "../interfaces";
import Router from "../router";
import { Option } from "../interfaces";
import {
  getAllPlaylists,
  addTrackToPlaylist,
} from "../composables/fetch/playlists";

import useQueueStore from "../stores/queue";
import useModalStore from "../stores/modal";
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

  const single_artist = track.artists.length === 1;

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

  const goToArtist = () => {
    if (single_artist) {
      return false;
    }

    return track.artists.map((artist) => {
      return <Option>{
        label: artist,
        action: () => console.log("artist"),
      };
    });
  };

  function addToPlaylist() {
    const new_playlist = <Option>{
      label: "New playlist",
      action: () => {
        modalStore().showNewPlaylistModal(track);
      },
    };

    return [new_playlist, separator, ...playlists];
  }

  const add_to_playlist: Option = {
    label: "Add to Playlist",
    children: addToPlaylist(),
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
    icon: "add_to_queue",
  };

  const go_to_folder: Option = {
    label: "Go to Folder",
    action: () => {
      Router.push({
        name: "FolderView",
        params: { path: track.folder },
        query: { highlight: track.uniq_hash },
      });
    },
    icon: "folder",
  };

  const go_to_artist: Option = {
    label: single_artist ? "Go to Artist" : "Go to Artists",
    icon: "artist",
    action: () => {
      if (single_artist) {
        console.log("Go to Artist");
      }
    },
    children: goToArtist(),
  };

  const go_to_alb_artist: Option = {
    label: "Go to Album Artist",
    action: () => console.log("Go to Album Artist"),
    icon: "artist",
  };

  const go_to_album: Option = {
    label: "Go to Album",
    action: () => {
      Router.push({
        name: "AlbumView",
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
    add_to_playlist,
    play_next,
    add_to_q,
    // add_to_fav,
    separator,
    go_to_folder,
    // go_to_artist,
    // go_to_alb_artist,
    go_to_album,
    // separator,
    // del_track,
  ];

  return options;
};
