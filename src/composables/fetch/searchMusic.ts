import state from "../state";
import axios from "axios";
import useAxios from "./useAxios";

const base_url = `${state.settings.uri}/search`;

const uris = {
  tracks: `${base_url}/tracks?q=`,
  albums: `${base_url}/albums?q=`,
  artists: `${base_url}/artists?q=`,
};

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
  const url = uris.tracks + encodeURIComponent(query.trim());
  return await fetchData(url);
}

async function searchAlbums(query: string) {
  const url = uris.albums + encodeURIComponent(query.trim());
  return await fetchData(url);
}

async function searchArtists(query: string) {
  const url = uris.artists + encodeURIComponent(query.trim());
  return await fetchData(url);
}

const loadmore_url = state.settings.uri + "/search/loadmore";

async function loadMoreTracks(index: number) {
  const response = await axios.get(loadmore_url, {
    params: {
      type: "tracks",
      index: index,
    },
  });

  return response.data;
}

async function loadMoreAlbums(index: number) {
  const response = await axios.get(loadmore_url, {
    params: {
      type: "albums",
      index: index,
    },
  });

  return response.data;
}

async function loadMoreArtists(index: number) {
  const response = await axios.get(loadmore_url, {
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

// TODO:
// Rewrite this module using `useAxios` hook
