import { defineStore } from "pinia";
import { Folder, Track } from "../../interfaces";

import fetchThem from "../../composables/fetch/folders";

export default defineStore("FolderDirs&Tracks", {
  state: () => ({
    path: <string>{},
    dirs: <Folder[]>[],
    tracks: <Track[]>[],
  }),
  actions: {
    async fetchAll(path: string) {
      const { tracks, folders } = await fetchThem(path);

      [this.path, this.dirs, this.tracks] = [path, folders, tracks];
    },
  },
});
