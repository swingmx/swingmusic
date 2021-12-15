import { ref } from "@vue/reactivity";

let home_url = "http://127.0.0.1:9876";

const getData = async (path) => {
  const songs = ref(null);
  const folders = ref(null);

  const res = await fetch(`${home_url}/?f=${path}`);

  if (!res.ok) {
    const message = `An erro has occured: ${res.status}`;
    throw new Error(message);
  }

  const data = await res.json();
  songs.value = data.songs;
  folders.value = data.folders;

  return { songs, folders };
};

export default getData;
