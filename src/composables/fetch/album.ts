import { paths } from "@/config";
import state from "../state";
import { AlbumInfo, Track } from "../../interfaces";
import useAxios from "./useAxios";
import { NotifType, useNotifStore } from "@/stores/notification";

const {
  album: albumUrl,
  albumartists: albumArtistsUrl,
  albumbio: albumBioUrl
} = paths.api

const getAlbumData = async (hash: string, ToastStore: typeof useNotifStore) => {
  interface AlbumData {
    info: AlbumInfo;
    tracks: Track[];
  }

  const { data, status } = await useAxios({
    url: albumUrl,
    props: {
      hash: hash,
    },
  });

  if (status == 204) {
    ToastStore().showNotification("Album not created yet!", NotifType.Error);
    return {
      info: {} as AlbumInfo,
      tracks: [],
    };
  }

  return data as AlbumData;
};

const getAlbumArtists = async (hash: string) => {
  const { data, error } = await useAxios({
    url: albumArtistsUrl,
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
    url: albumBioUrl,
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
