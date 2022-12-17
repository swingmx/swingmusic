import { paths } from "@/config";
import useAxios from "./useAxios";
import { Artist, Track, Album } from "@/interfaces";

const getArtistData = async (hash: string, limit: number = 5) => {
  interface ArtistData {
    artist: Artist;
    tracks: Track[];
  }

  const { data, error } = await useAxios({
    get: true,
    url: paths.api.artist + `/${hash}?limit=${limit}`,
  });

  if (error) {
    console.error(error);
  }

  return data as ArtistData;
};

const getArtistAlbums = async (hash: string, all = false, limit = 6) => {
  interface ArtistAlbums {
    albums: Album[];
    eps: Album[];
    singles: Album[];
    appearances: Album[];
    artistname: string;
  }

  const { data, error } = await useAxios({
    get: true,
    url: paths.api.artist + `/${hash}/albums?limit=${limit}&all=${all}`,
  });

  if (error) {
    console.error(error);
  }

  return data as ArtistAlbums;
};

const getArtistTracks = async (hash: string, offset: number = 0, limit = 6) => {
  const { data, error } = await useAxios({
    get: true,
    url: paths.api.artist + `/${hash}/tracks?offset=${offset}&limit=${limit}`,
  });

  if (error) {
    console.error(error);
  }

  return data.tracks as Track[];
};

export { getArtistData, getArtistAlbums, getArtistTracks };
