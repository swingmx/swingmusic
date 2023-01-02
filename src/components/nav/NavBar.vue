<template>
  <div class="topnav">
    <div class="left">
      <NavButtons />

      <div class="info">
        <SettingsTitle
          v-if="$route.name == Routes.settings"
          :text="'Settings'"
        />
        <FolderTitle v-if="$route.name == Routes.folder" :subPaths="subPaths" />
        <SearchTitle v-if="$route.name == Routes.search" />
        <PlaylistsTitle v-if="$route.name == Routes.playlists" />
        <QueueTitle v-if="$route.name == Routes.queue" />
        <ArtistDiscographyTitle
          v-if="$route.name == Routes.artistDiscography"
        />
        <SimpleNav
          v-if="$route.name == Routes.artistTracks"
          :text="$route.query.artist as string || 'Artist Tracks'"
        />
        <SimpleNav
          v-if="$route.name === Routes.favorites"
          :text="'Favorites ❤️'"
        />
        <SimpleNav
          v-if="$route.name === Routes.favoriteAlbums"
          :text="'Favorite Albums ❤️'"
        />
        <SimpleNav
          v-if="$route.name === Routes.favoriteArtists"
          :text="'Favorite Artists ❤️'"
        />
        <SimpleNav
          v-if="$route.name === Routes.favoriteTracks"
          :text="'Favorite Tracks ❤️'"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

import { subPath } from "@/interfaces";
import { Routes } from "@/router/routes";
import { createSubPaths } from "@/utils";

import NavButtons from "./NavButtons.vue";

import FolderTitle from "./Titles/Folder.vue";
import SimpleNav from "./Titles/SimpleNav.vue";
import PlaylistsTitle from "./Titles/PlaylistsTitle.vue";
import QueueTitle from "./Titles/QueueTitle.vue";
import SearchTitle from "./Titles/SearchTitle.vue";
import SettingsTitle from "./Titles/SettingsTitle.vue";
import ArtistDiscographyTitle from "./Titles/ArtistDiscographyTitle.vue";

const route = useRoute();
const subPaths = ref<subPath[]>([]);

watch(
  () => route.name,
  (newRoute) => {
    switch (newRoute) {
      case Routes.folder:
        let oldpath = "";
        [oldpath, subPaths.value] = createSubPaths(
          route.params.path as string,
          oldpath
        );

        watch(
          () => route.params.path,
          (newPath) => {
            newPath = newPath as string;
            if (newPath == undefined) return;

            [oldpath, subPaths.value] = createSubPaths(newPath, oldpath);
          }
        );
        break;
      default:
        break;
    }
  }
);
</script>

<style lang="scss">
.topnav {
  display: grid;
  grid-template-columns: 1fr min-content;
  width: 100%;
  padding: 0 1.25rem;

  .left {
    display: grid;
    grid-template-columns: max-content 1fr;
    gap: 1rem;
    height: 2.25rem;

    .info {
      margin: auto 0;

      .title {
        font-size: 1.5rem;
        font-weight: bold;
        display: flex;
        align-items: center;
      }
    }
  }

  .center {
    display: grid;
    place-items: center;
    margin-right: 1rem;
  }
}
</style>
