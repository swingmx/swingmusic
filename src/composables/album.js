import axios from "axios";
import state from "./state";

const getAlbumTracks = async (album, artist) => {
  let data = {};

  await axios
    .post(state.settings.uri + "/album/tracks", {
      album: album,
      artist: artist,
    })
    .then((res) => {
      data = res.data;
    })
    .catch((err) => {
      console.error(err);
    });

  return data;
};

const getAlbumArtists = async (album, artist) => {
  let artists = [];

  await axios
    .post(state.settings.uri + "/album/artists", {
      album: album,
      artist: artist,
    })
    .then((res) => {
      artists = res.data.artists;
    })
    .catch((err) => {
      console.error(err);
    });

  return artists;
};

const getAlbumBio = async (name, artist) => {
  const res = await fetch(
    state.settings.uri +
      "/album/" +
      encodeURIComponent(name.replaceAll("/", "|")) +
      "/" +
      encodeURIComponent(artist.replaceAll("/", "|")) +
      "/bio"
  );

  if (!res.ok) {
    const message = `An error has occurred: ${res.status}`;
    throw new Error(message);
  }

  const data = await res.json();
  return data.bio;
};

export default {
  getAlbumTracks,
  getAlbumArtists,
  getAlbumBio,
};
