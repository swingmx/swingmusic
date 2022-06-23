import state from "../state";
import { AlbumInfo, Track } from "../../interfaces";
import useAxios from "../useAxios";
import { NotifType, useNotifStore } from "@/stores/notification";

const getAlbumData = async (
  album: string,
  artist: string,
  ToastStore: typeof useNotifStore
) => {
  const url = state.settings.uri + "/album";

  interface AlbumData {
    info: AlbumInfo;
    tracks: Track[];
  }

  const { data, status } = await useAxios({
    url,
    props: {
      album: album,
      artist: artist,
    },
  });

  if (status == 204) {
    ToastStore().showNotification("Album not created yet!", NotifType.Error);
    return {
      info: {
        album: album,
        artist: artist,
      },
      tracks: [],
    };
  }

  return data as AlbumData;
};

const getAlbumArtists = async (album: string, artist: string) => {
  const { data, error } = await useAxios({
    url: state.settings.uri + "/album/artists",
    props: {
      album: album,
      artist: artist,
    },
  });

  if (error) {
    console.error(error);
  }

  return data.artists;
};

const getAlbumBio = async (album: string, albumartist: string) => {
  const { data, status } = await useAxios({
    url: state.settings.uri + "/album/bio",
    props: {
      album: album,
      albumartist: albumartist,
    },
  });

  if (data) {
    return data.bio;
  }

  if (status == 404) {
    return null;
  }
};

export { getAlbumData as getAlbumTracks, getAlbumArtists, getAlbumBio };
