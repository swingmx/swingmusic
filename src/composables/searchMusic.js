import state from "./state.js";

const base_url = `${state.settings.uri}/search?q=`;

async function search(query) {
  state.loading.value = true;
  const url = base_url + encodeURIComponent(query.trim());

  const res = await fetch(url);

  if (!res.ok) {
    const message = `An error has occured: ${res.status}`;
    throw new Error(message);
  }

  const data = await res.json();

  state.loading.value = false;

  return {
    tracks: data.data[0],
    albums: data.data[1],
    artists: data.data[2],
  };
}

export default search;
