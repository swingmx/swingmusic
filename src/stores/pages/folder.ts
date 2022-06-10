import { defineStore } from "pinia";
import { Folder, Track } from "../../interfaces";

import fetchThem from "../../composables/getFilesAndFolders";

export default defineStore("FolderDirs&Tracks", {
  state: () => ({
    path: <string>{},
    dirs: <Folder[]>[],
    tracks: <Track[]>[],
  }),
  actions: {
    async fetchAll(path: string) {
      const { tracks, folders } = await fetchThem(path);

      this.path = path;
      this.dirs = folders;
      this.tracks = tracks;
    },
  },
});
