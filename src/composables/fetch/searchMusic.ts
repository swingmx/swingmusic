import { paths } from "@/config";
import axios from "axios";
import useAxios from "./useAxios";

const {
  tracks: searchTracksUrl,
  albums: searchAlbumsUrl,
  artists: searchArtistsUrl,
  load: loadMoreUrl,
} = paths.api.search;

/**
 * Fetch data from url
 * @param url url to fetch json from
 * @returns promise that resolves to the JSON
 */
async function fetchData(url: string) {
  const { data } = await useAxios({
    url: url,
    get: true,
  });

  return data;
}

async function searchTracks(query: string) {
  const url = searchTracksUrl + encodeURIComponent(query.trim());
  return await fetchData(url);
}

async function searchAlbums(query: string) {
  const url = searchAlbumsUrl + encodeURIComponent(query.trim());
  return await fetchData(url);
}

async function searchArtists(query: string) {
  const url = searchArtistsUrl + encodeURIComponent(query.trim());
  return await fetchData(url);
}

async function loadMoreTracks(index: number) {
  const response = await axios.get(loadMoreUrl, {
    params: {
      type: "tracks",
      index: index,
    },
  });

  return response.data;
}

async function loadMoreAlbums(index: number) {
  const response = await axios.get(loadMoreUrl, {
    params: {
      type: "albums",
      index: index,
    },
  });

  return response.data;
}

async function loadMoreArtists(index: number) {
  const response = await axios.get(loadMoreUrl, {
    params: {
      type: "artists",
      index: index,
    },
  });

  return response.data;
}

export {
  searchTracks,
  searchAlbums,
  searchArtists,
  loadMoreTracks,
  loadMoreAlbums,
  loadMoreArtists,
};

// TODO: Rewrite this module using `useAxios` hook
