import state from "./state.js";

const base_url = "http://0.0.0.0:9876/search?q=";

async function search(query) {
  state.loading.value = true;
  const url = base_url + encodeURIComponent(query);

  const res = await fetch(url);

  if (!res.ok) {
    const message = `An error has occured: ${res.status}`;
    throw new Error(message);
  }

  const data = await res.json();
  console.log(data.data[1]);

  state.loading.value = false;

  return {
    tracks: data.data[0],
    albums: data.data[1],
    artists: data.data[2],
  };
}

export default search;
