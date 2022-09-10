import { defineStore } from "pinia";
import { ComputedRef } from "vue";

import { useFuse } from "@/utils";

import { FuseTrackOptions } from "@/composables/enums";
import fetchThem from "@/composables/fetch/folders";
import { Folder, FuseResult, Track } from "@/interfaces";

export default defineStore("FolderDirs&Tracks", {
  state: () => ({
    query: "",
    path: <string>{},
    allDirs: <Folder[]>[],
    allTracks: <Track[]>[],
  }),
  actions: {
    async fetchAll(path: string) {
      const { tracks, folders } = await fetchThem(path);

      [this.path, this.allDirs, this.allTracks] = [path, folders, tracks];
    },
    resetQuery() {
      this.query = "";
    },
  },
  getters: {
    filteredTracks(): ComputedRef<FuseResult[]> {
      return useFuse(this.query, this.allTracks, FuseTrackOptions);
    },
    tracks(): Track[] {
      const tracks = this.filteredTracks.value.map((result: FuseResult) => {
        const t = {
          ...result.item,
          index: result.refIndex,
        };

        return t;
      });

      return tracks;
    },
    dirs(): Folder[] {
      const dirs = useFuse(this.query, this.allDirs, {
        keys: ["name"],
      });

      return dirs.value.map((result) => {
        return result.item;
      });
    },
  },
});
