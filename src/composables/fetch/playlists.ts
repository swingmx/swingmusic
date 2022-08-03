import { Artist } from "../../interfaces";
import { Playlist, Track } from "../../interfaces";
import { Notification, NotifType } from "../../stores/notification";
import state from "../state";
import useAxios from "./useAxios";
/**
 * Creates a new playlist on the server.
 * @param playlist_name The name of the playlist to create.
 */
async function createNewPlaylist(playlist_name: string, track?: Track) {
  const { data, status } = await useAxios({
    url: state.settings.uri + "/playlist/new",
    props: {
      name: playlist_name,
    },
  });

  if (status == 201) {
    new Notification("✅ Playlist created successfullly!");

    if (track) {
      setTimeout(() => {
        addTrackToPlaylist(data.playlist, track);
      }, 1000);
    }

    return {
      success: true,
      playlist: data.playlist as Playlist,
    };
  }

  new Notification("That playlist already exists", NotifType.Error);

  return {
    success: false,
    playlist: <Playlist>{},
  };
}

/**
 * Fetches all playlists from the server.
 * @returns {Promise<Playlist[]>} A promise that resolves to an array of playlists.
 */
async function getAllPlaylists(): Promise<Playlist[]> {
  const { data, error } = await useAxios({
    url: state.settings.uri + "/playlists",
    get: true,
  });

  if (error) console.error(error);

  if (data) {
    return data.data;
  }

  return [];
}

async function addTrackToPlaylist(playlist: Playlist, track: Track) {
  const uri = `${state.settings.uri}/playlist/${playlist.playlistid}/add`;

  const { status } = await useAxios({
    url: uri,
    props: {
      track: track.trackid,
    },
  });

  if (status == 409) {
    new Notification("Track already exists in playlist", NotifType.Info);
    return;
  }

  new Notification(track.title + " added to " + playlist.name);
}

async function getPlaylist(pid: string) {
  const uri = state.settings.uri + "/playlist/" + pid;

  interface PlaylistData {
    info: Playlist;
    tracks: Track[];
  }

  const { data, error } = await useAxios({
    url: uri,
    get: true,
  });

  if (error) {
    new Notification("Something funny happened!", NotifType.Error);
  }

  if (data) {
    return data as PlaylistData;
  }

  return null;
}

async function updatePlaylist(pid: string, playlist: FormData, pStore: any) {
  const uri = state.settings.uri + "/playlist/" + pid + "/update";

  const { data, error } = await useAxios({
    url: uri,
    put: true,
    props: playlist,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  if (error) {
    new Notification("Something funny happened!", NotifType.Error);
  }

  if (data) {
    pStore.updatePInfo(data.data);
    new Notification("Playlist updated!");
  }
}

/**
 * Gets the artists in a playlist.
 * @param pid The playlist id to fetch tracks for.
 * @returns {Promise<Artist[]>} A promise that resolves to an array of artists.
 */
export async function getPlaylistArtists(pid: string): Promise<Artist[]> {
  const uri = state.settings.uri + "/playlist/artists";

  const { data, error } = await useAxios({
    url: uri,
    props: {
      pid: pid,
    },
  });

  if (error) {
    new Notification("Something funny happened!", NotifType.Error);
  }

  if (data) {
    return data.data as Artist[];
  }

  return [];
}

export {
  createNewPlaylist,
  getAllPlaylists,
  addTrackToPlaylist,
  getPlaylist,
  updatePlaylist,
};
