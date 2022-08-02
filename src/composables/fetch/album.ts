import state from "../state";
import { AlbumInfo, Track } from "../../interfaces";
import useAxios from "./useAxios";
import { NotifType, useNotifStore } from "@/stores/notification";

const getAlbumData = async (hash: string, ToastStore: typeof useNotifStore) => {
  const url = state.settings.uri + "/album";

  interface AlbumData {
    info: AlbumInfo;
    tracks: Track[];
  }

  const { data, status } = await useAxios({
    url,
    props: {
      hash: hash,
    },
  });

  if (status == 204) {
    ToastStore().showNotification("Album not created yet!", NotifType.Error);
    return {
      info: {
        album: "",
        artist: "",
        colors: []
      },
      tracks: [],
    };
  }

  return data as AlbumData;
};

const getAlbumArtists = async (hash: string) => {
  const { data, error } = await useAxios({
    url: state.settings.uri + "/album/artists",
    props: {
      hash: hash,
    },
  });

  if (error) {
    console.error(error);
  }

  return data.artists;
};

const getAlbumBio = async (hash: string) => {
  const { data, status } = await useAxios({
    url: state.settings.uri + "/album/bio",
    props: {
      hash: hash,
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
