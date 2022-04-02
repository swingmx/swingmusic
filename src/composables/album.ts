import axios from "axios";
import state from "./state";
import { AlbumInfo, Track } from "../interfaces";

const getAlbumTracks = async (album: string, artist: string) => {
  let data = {
    info: <AlbumInfo>{},
    tracks: <Track[]>[],
  };

  await axios
    .post(state.settings.uri + "/album/tracks", {
      album: album,
      artist: artist,
    })
    .then((res) => {
      data.info = res.data.info;
      data.tracks = res.data.songs;
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

const getAlbumBio = async (album: string, albumartist: string) => {
  let bio = null;

  await axios
    .post(state.settings.uri + "/album/bio", {
      album: album,
      albumartist: albumartist,
    })
    .then((res) => {
      bio = res.data.bio;
    })
    .catch((err) => {
      if (err.response.status === 404) {
        bio = null;
      }
    });

  return bio;
};

export { getAlbumTracks, getAlbumArtists, getAlbumBio };
