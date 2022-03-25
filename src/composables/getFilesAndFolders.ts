import axios from "axios";
import { Folder, Track } from "../interfaces";
import state from "./state";

export default async function (path: string) {
  let tracks = Array<Track>();
  let folders = Array<Folder>();

  await axios
    .post(`${state.settings.uri}/folder`, {
      folder: path,
    })
    .then((res) => {
      tracks = res.data.tracks;
      folders = res.data.folders;
    })
    .catch((err) => {
      console.error(err);
    });

  return { tracks, folders };
}
