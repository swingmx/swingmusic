<template>
  <div class="nav-queue-title">
    <div class="first noscroll">
      <router-link :to="(location as RouteLocationRaw)">
        <button>Go to source</button>
      </router-link>
      <div class="playing-from">
        <div class="border rounded-sm pad-sm">
          <source-icon />
          <b class="ellip">{{ name }}</b>
        </div>
      </div>
    </div>
    <QueueActions />
  </div>
</template>

<script setup lang="ts">
import QueueActions from "@/components/RightSideBar/Queue/QueueActions.vue";
import { FromOptions, Routes } from "@/composables/enums";
import useQueueStore from "@/stores/queue";

import FolderSvg from "@/assets/icons/folder.svg";
import SearchSvg from "@/assets/icons/search.svg";
import AlbumSvg from "@/assets/icons/album.svg";
import PlaylistSvg from "@/assets/icons/playlist.svg";

import { RouteLocationRaw } from "vue-router";

const queue = useQueueStore();

const { from: source } = queue;

function getSource() {
  switch (source.type) {
    case FromOptions.album:
      return {
        name: source.name,
        icon: AlbumSvg,
        location: {
          name: Routes.album,
          params: {
            hash: source.hash,
          },
        },
      };

    case FromOptions.folder:
      return {
        name: source.name,
        icon: FolderSvg,
        location: {
          name: Routes.folder,
          params: {
            path: source.path,
          },
        },
      };

    case FromOptions.playlist:
      return {
        name: source.name,
        icon: PlaylistSvg,
        location: {
          name: Routes.playlist,
          params: {
            pid: source.playlistid,
          },
        },
      };

    case FromOptions.search:
      return {
        name: `Search for: "${source.query}"`,
        icon: SearchSvg,
        location: {
          name: Routes.search,
          params: {
            query: source.query,
          },
        },
      };

    default:
      return { name: "Ghost source" };
  }
}

const { name, icon: SourceIcon, location } = getSource();
</script>

<style lang="scss">
.nav-queue-title {
  display: grid;
  grid-template-columns: 1fr max-content;
  gap: 1rem;
  align-items: center;

  .first {
    width: 100%;
    display: grid;
    grid-template-columns: max-content 1fr;
    gap: 1rem;

    .playing-from {
      display: flex;
      align-items: center;
      gap: $small;
      opacity: 0.75;

      .border {
        display: grid;
        grid-template-columns: max-content 1fr;
        align-items: center;
        padding: $smaller $small;
      }

      svg {
        transform: scale(0.9);
      }
    }

    button {
      cursor: pointer;
    }
  }

  .queue-actions {
    margin: 0;
  }
}
</style>
