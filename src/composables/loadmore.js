import axios from "axios";

const url = "http://10.5.8.182:9876/search/loadmore";

async function loadMoreTracks(start) {
  const response = await axios.get(url, {
    params: {
      type: "tracks",
      start: start,
    },
  });

  return response.data;
}

async function loadMoreAlbums(start) {
  const response = await axios.get(url, {
    params: {
      type: "albums",
      start: start,
    },
  });

  return response.data;
}

async function loadMoreArtists(start) {
  const response = await axios.get(url, {
    params: {
      type: "artists",
      start: start,
    },
  });

  return response.data;
}

export default {
  loadMoreTracks,
  loadMoreAlbums,
  loadMoreArtists,
};
