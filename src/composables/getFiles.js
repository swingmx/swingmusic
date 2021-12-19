import { ref } from "@vue/reactivity";

let folders_uri = "http://127.0.0.1:9876";

const getData = async (path, last_id) => {
  let url;
  const songs = ref(null);
  const folders = ref(null);
  
  const encoded_path = encodeURIComponent(path.replaceAll("/", "|"));

  if (last_id) {
    url = `${folders_uri}/f/${encoded_path}::${last_id}`;
  } else {
    url = url = `${folders_uri}/f/${encoded_path}`;
  }

  const res = await fetch(url);

  if (!res.ok) {
    const message = `An erro has occured: ${res.status}`;
    throw new Error(message);
  }

  const data = await res.json();

  songs.value = data.files;
  folders.value = data.folders;

  return { songs, folders };
};

export default getData;
