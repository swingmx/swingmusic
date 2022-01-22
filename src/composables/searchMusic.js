import state from "./state.js";

const base_url = "http://0.0.0.0:9876/search?q=";

async function search(query) {
  const url = base_url + encodeURIComponent(query);

  const res = await fetch(url);
    const json = await res.json();
    state.search_tracks.value = json.songs;
    state.search_albums.value = json.albums;
    state.search_artists.value = json.artists;

    console.log(state.search_tracks.value);
}

export default search;