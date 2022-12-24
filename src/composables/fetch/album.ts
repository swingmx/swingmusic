import { paths } from "@/config";
import { NotifType, useNotifStore } from "@/stores/notification";
import { Album, Track } from "../../interfaces";
import useAxios from "./useAxios";

const {
  album: albumUrl,
  albumartists: albumArtistsUrl,
  albumbio: albumBioUrl,
  albumsByArtistUrl,
} = paths.api;

const getAlbumData = async (hash: string, ToastStore: typeof useNotifStore) => {
  interface AlbumData {
    info: Album;
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

const getAlbumsFromArtist = async (
  albumartists: string,
  limit: number = 2,
  exclude: string
) => {
  const { data } = await useAxios({
    url: albumsByArtistUrl,
    props: {
      albumartists: albumartists,
      limit: limit,
      exclude: exclude,
    },
  });

  if (data) {
    return data.data;
  }

  return [];
};

async function getAlbumTracks(albumhash: string): Promise<Track[]> {
  const { data } = await useAxios({
    url: albumUrl + `/${albumhash}/` + "tracks",
    get: true,
  });

  return data.tracks;
}

export {
  getAlbumData as getAlbum,
  getAlbumTracks,
  getAlbumArtists,
  getAlbumBio,
  getAlbumsFromArtist,
};
