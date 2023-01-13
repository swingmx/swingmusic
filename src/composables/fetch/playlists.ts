import { paths } from "@/config";
import { Artist, Playlist, Track } from "../../interfaces";
import { Notification, NotifType } from "../../stores/notification";
import useAxios from "./useAxios";

const {
  new: newPlaylistUrl,
  all: allPlaylistsUrl,
  base: basePlaylistUrl,
  artists: playlistArtistsUrl,
} = paths.api.playlist;

/**
 * Creates a new playlist on the server.
 * @param playlist_name The name of the playlist to create.
 */
export async function createNewPlaylist(playlist_name: string, track?: Track) {
  const { data, status } = await useAxios({
    url: newPlaylistUrl,
    props: {
      name: playlist_name,
    },
  });

  if (status == 201) {
    new Notification("Playlist created successfullly!");

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

  let message = "Something went wrong";

  if (status == 409) {
    message = "That playlist already exists";
  }

  new Notification(message, NotifType.Error);

  return {
    success: false,
    playlist: <Playlist>{},
  };
}

/**
 * Fetches all playlists from the server.
 * @returns {Promise<Playlist[]>} A promise that resolves to an array of playlists.
 */
export async function getAllPlaylists(): Promise<Playlist[]> {
  const { data, error } = await useAxios({
    url: allPlaylistsUrl,
    get: true,
  });

  if (error) console.error(error);

  if (data) {
    return data.data;
  }

  return [];
}

export async function addTrackToPlaylist(playlist: Playlist, track: Track) {
  const uri = `${basePlaylistUrl}/${playlist.id}/add`;

  const { status } = await useAxios({
    url: uri,
    props: {
      track: track.trackhash,
    },
  });

  if (status == 409) {
    new Notification("Track already exists in playlist");
    return;
  }

  new Notification(
    track.title + " added to " + playlist.name,
    NotifType.Success
  );
}

export async function getPlaylist(pid: string) {
  const uri = `${basePlaylistUrl}/${pid}`;

  interface PlaylistData {
    info: Playlist;
    tracks: Track[];
  }

  const { data, status } = await useAxios({
    url: uri,
    get: true,
  });

  if (status == 404) {
    new Notification("Playlist not found", NotifType.Error);
  }

  if (data) {
    return data as PlaylistData;
  }

  return null;
}

export async function updatePlaylist(
  pid: string,
  playlist: FormData,
  pStore: any
) {
  const uri = `${basePlaylistUrl}/${pid}/update`;

  const { data, status } = await useAxios({
    url: uri,
    put: true,
    props: playlist,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  if (status == 400) {
    new Notification("Failed: Unsupported image", NotifType.Error);
    return;
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
  const { data, error } = await useAxios({
    url: playlistArtistsUrl,
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

export async function deletePlaylist(pid: string) {
  const { status } = await useAxios({
    url: paths.api.playlist.base + "/delete",
    props: {
      pid,
    },
  });

  if (status == 200) {
    new Notification("Playlist deleted", NotifType.Success);
  }
}

export async function updateBannerPos(pid: number, pos: number) {
  const { status } = await useAxios({
    url: paths.api.playlist.base + `/${pid}/set-image-pos`,
    props: {
      pos,
    },
  });

  if (status === 200) {
    new Notification("Image position saved", NotifType.Info);
    return;
  }

  new Notification("Unable to save image position", NotifType.Error);
}
