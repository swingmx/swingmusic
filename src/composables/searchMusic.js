import state from "./state.js";

const base_url = "http://127.0.0.1:9876/search?q=";

async function search(query) {
  const url = base_url + query;

  const res = await fetch(url);
    const json = await res.json();
    state.search_tracks.value = json.songs;
    state.search_albums.value = json.albums;
    state.search_artists.value = json.artists;
    console.log(state.search);
}

export default search;