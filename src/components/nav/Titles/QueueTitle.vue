<template>
  <div class="nav-queue-title">
    <div class="first no-scroll">
      <div class="playing-from">
        <router-link :to="(location as RouteLocationRaw)">
          <div class="border rounded-sm pad-sm">
            <SourceIcon v-if="SourceIcon" />
            <b class="ellip">{{ name }}</b>
          </div>
        </router-link>
      </div>
    </div>
    <QueueActions />
  </div>
</template>

<script setup lang="ts">
import QueueActions from "@/components/RightSideBar/Queue/QueueActions.vue";
import { FromOptions } from "@/composables/enums";
import useQueueStore from "@/stores/queue";
import { Routes } from "@/router/routes";

import AlbumSvg from "@/assets/icons/album.svg";
import FolderSvg from "@/assets/icons/folder.svg";
import PlaylistSvg from "@/assets/icons/playlist.svg";
import SearchSvg from "@/assets/icons/search.svg";
import ArtistSvg from "@/assets/icons/artist.svg";

import { RouteLocationRaw } from "vue-router";
import HeartSvg from "@/assets/icons/heart.fill.svg";

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
            hash: source.albumhash,
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
            pid: source.id,
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
            page: "tracks",
          },
        },
      };

    case FromOptions.artist:
      return {
        name: source.artistname,
        icon: ArtistSvg,
        location: {
          name: Routes.artist,
          params: {
            hash: source.artisthash,
          },
        },
      };

    case FromOptions.favorite:
      return {
        name: "Favorite tracks",
        icon: HeartSvg,
        location: {
          name: Routes.favoriteTracks,
        },
      };

    default:
      return { name: "👻 No source", location: {} };
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
    .playing-from {
      display: flex;
      align-items: center;
      gap: $small;
      opacity: 0.75;

      .border {
        cursor: pointer;
        display: grid;
        grid-template-columns: max-content 1fr;
        align-items: center;
        padding: $smaller $small;
        height: 100%;

        &:hover {
          background-color: $darkestblue;
          border: solid 1px $darkestblue;
        }
      }

      svg {
        transform: scale(0.9);
      }
    }
  }

  .queue-actions {
    margin: 0;
  }
}
</style>
