import axios from "axios";
import { Playlist } from "../interfaces";
import { Notification } from "../stores/notification";
import state from "./state";

/**
 * Creates a new playlist on the server.
 * @param playlist_name The name of the playlist to create.
 */
async function createNewPlaylist(playlist_name: string) {
  await axios
    .post(state.settings.uri + "/playlist/new", {
      name: playlist_name,
    })
    .then((res) => {
      console.log(res.data);
      new Notification("Playlist created!");
    })
    .catch((err) => {
      console.error(err);
    });
}

/**
 * Fetches all playlists from the server.
 * @returns {Promise<Playlist[]>} A promise that resolves to an array of playlists.
 */
async function getAllPlaylists(): Promise<Playlist[]> {
  let playlists = <Playlist[]>[];

  const newLocal = `${state.settings.uri}/playlists`;

  await axios
    .get(newLocal)
    .then((res) => {
      playlists = res.data.data;
    })
    .catch((err) => {
      console.error(err);
    });

  return playlists;
}

export { createNewPlaylist, getAllPlaylists };
