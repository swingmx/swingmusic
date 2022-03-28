import axios from "axios";
import { Playlist, Track } from "../interfaces";
import { Notification, NotifType } from "../stores/notification";
import state from "./state";

/**
 * Creates a new playlist on the server.
 * @param playlist_name The name of the playlist to create.
 */
async function createNewPlaylist(playlist_name: string, track?: Track) {
  let status = false;

  await axios
    .post(state.settings.uri + "/playlist/new", {
      name: playlist_name,
    })
    .then((res) => {
      new Notification("✅ Playlist created successfullly!");

      if (track) {
        setTimeout(() => {
          addTrackToPlaylist(res.data.playlist, track);
        }, 1000);
      }

      status = true;
    })
    .catch((err) => {
      if (err.response.status == 409) {
        new Notification(
          "That playlist already exists ... you might want to try another name!",
          NotifType.Error
        );
      }
    });

  return status;
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

async function addTrackToPlaylist(playlist: Playlist, track: Track) {
  const uri = `${state.settings.uri}/playlist/${playlist.playlistid}/add`;
  console.log(track.trackid, playlist.playlistid);

  await axios
    .post(uri, { track: track.trackid })
    .then(() => {
      new Notification(track.title + " added to " + playlist.name);
    })
    .catch((error) => {
      if (error.response.status == 409) {
        new Notification("Track already exists in playlist", NotifType.Info);
      }
    });
}

async function getPTracks(playlistid: string) {
  const uri = state.settings.uri + "/playlist/" + playlistid;

  let tracks: Track[] = [];

  await axios
    .get(uri)
    .then((res) => {
      tracks = res.data.data;
    })
    .catch((err) => {
      new Notification("Something funny happened!", NotifType.Error);
      throw new Error(err);
    });

  return tracks;
}

async function getPlaylist(pid: string) {
  const uri = state.settings.uri + "/playlist/" + pid;

  let playlist: Playlist;

  await axios
    .get(uri)
    .then((res) => {
      playlist = res.data.data;
    })
    .catch((err) => {
      new Notification("Something funny happened!", NotifType.Error);
      throw new Error(err);
    });

  return playlist;
}

export { createNewPlaylist, getAllPlaylists, addTrackToPlaylist, getPTracks, getPlaylist };
