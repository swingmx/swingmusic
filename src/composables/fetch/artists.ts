import { paths } from "@/config";
import useAxios from "./useAxios";
import { Artist, Track, Album } from "@/interfaces";

const getArtistData = async (hash: string) => {
  interface ArtistData {
    artist: Artist;
    albums: Album[];
    tracks: Track[];
  }

  const { data, error } = await useAxios({
    get: true,
    url: paths.api.artist + `/${hash}?limit=6`,
  });

  if (error) {
    console.error(error);
  }

  console.log(data);

  return data as ArtistData;
};

export { getArtistData };
