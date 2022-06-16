import axios, { AxiosError } from "axios";
import state from "../state";
import { AlbumInfo, Track } from "../../interfaces";
import useAxios from "../useAxios";

const getAlbumTracks = async (album: string, artist: string) => {
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

  if (status == 404) {
    return {
      info: {},
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

export { getAlbumTracks, getAlbumArtists, getAlbumBio };
