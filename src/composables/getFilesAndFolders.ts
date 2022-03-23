import axios from "axios";
import state from "./state";
import { Track, Folder } from "../interfaces";

let base_uri = "http://127.0.0.1:9876/";

const getTracksAndDirs = async (path) => {
  let url;

  const encoded_path = encodeURIComponent(path.replaceAll("/", "|"));
  url = url = `${base_uri}/f/${encoded_path}`;

  const res = await fetch(url);

  if (!res.ok) {
    const message = `An error has occurred: ${res.status}`;
    throw new Error(message);
  }

  const data = await res.json();

  const songs = data.files;
  const folders = data.folders;

  return { songs, folders };
};

async function fetchThat(path: string) {
  let tracks = Array<Track>();
  let folders = Array<Folder>();

  await axios
    .post(state.settings.uri + "/folder", {
      folder: path,
    })
    .then((res) => {
      tracks = res.data.tracks;
      folders = res.data.folders;
      console.log(tracks)
    })
    .catch((err) => {
      console.error(err);
    });

  return { tracks, folders };
}

export default fetchThat;
