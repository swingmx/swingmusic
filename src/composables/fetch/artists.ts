import { paths } from "@/config";
import useAxios from "./useAxios";
import { Artist, Track, Album } from "@/interfaces";

const getArtistData = async (hash: string) => {
  interface ArtistData {
    artist: Artist;
    tracks: Track[];
  }

  const { data, error } = await useAxios({
    get: true,
    url: paths.api.artist + `/${hash}`,
  });

  if (error) {
    console.error(error);
  }

  return data as ArtistData;
};

const getArtistAlbums = async (hash: string, limit = 6) => {
  const { data, error } = await useAxios({
    get: true,
    url: paths.api.artist + `/${hash}/albums?limit=${limit}`,
  });

  if (error) {
    console.error(error);
  }

  return data.albums as Album[];
};

export { getArtistData, getArtistAlbums };
