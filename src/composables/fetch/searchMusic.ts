import state from "../state";
import axios from "axios";

const base_url = `${state.settings.uri}/search`;

const uris = {
  tracks: `${base_url}/tracks?q=`,
  albums: `${base_url}/albums?q=`,
  artists: `${base_url}/artists?q=`,
};

async function searchTracks(query: string) {
  const url = uris.tracks + encodeURIComponent(query.trim());

  const res = await fetch(url);

  if (!res.ok) {
    const message = `An error has occured: ${res.status}`;
    throw new Error(message);
  }

  const data = await res.json();

  return data;
}

async function searchAlbums(query: string) {
  const url = uris.albums + encodeURIComponent(query.trim());

  const res = await axios.get(url);
  return res.data;
}

async function searchArtists(query: string) {
  const url = uris.artists + encodeURIComponent(query.trim());

  const res = await axios.get(url);
  return res.data;
}

const url = state.settings.uri + "/search/loadmore";

async function loadMoreTracks(index: number) {
  const response = await axios.get(url, {
    params: {
      type: "tracks",
      index: index,
    },
  });

  return response.data;
}

async function loadMoreAlbums(index: number) {
  const response = await axios.get(url, {
    params: {
      type: "albums",
      index: index,
    },
  });

  return response.data;
}

async function loadMoreArtists(index: number) {
  const response = await axios.get(url, {
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
