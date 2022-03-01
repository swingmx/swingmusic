import Router from "@/router";

import album from "./album.js";
import state from "./state.js";

async function toAlbum(title, artist) {
  console.log("routing to album");

  state.loading.value = true;
  await album
    .getAlbumTracks(title, artist)
    .then((data) => {
      state.album.tracklist = data.songs;
      state.album.info = data.info;
    })
    .then(
      await album.getAlbumArtists(title, artist).then((data) => {
        state.album.artists = data;
      })
    )
    .then(
      album.getAlbumBio(title, artist).then((data) => {
        if (data === "None") {
          state.album.bio = null;
        } else {
          state.album.bio = data;
        }
      })
    )
    .then(() => {
      Router.push({
        name: "AlbumView",
        params: {
          album: title,
          artist: artist,
        },
      });
      state.loading.value = false;
    })
    .catch((error) => {
      console.log(error);
    });
}

export default {
  toAlbum,
};
