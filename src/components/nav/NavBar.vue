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
        <ArtistTracksTitle v-if="$route.name == Routes.artistTracks" />
        <FavoritesNav v-if="$route.name === Routes.favorites" />
        <FavoriteAlbumsNav v-if="$route.name === Routes.favoriteAlbums" />
        <FavoriteTracksNav v-if="$route.name === Routes.favoriteTracks" />
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
import PlaylistsTitle from "./Titles/PlaylistsTitle.vue";
import QueueTitle from "./Titles/QueueTitle.vue";
import SearchTitle from "./Titles/SearchTitle.vue";
import SettingsTitle from "./Titles/SettingsTitle.vue";
import ArtistDiscographyTitle from "./Titles/ArtistDiscographyTitle.vue";
import ArtistTracksTitle from "./Titles/ArtistTracksTitle.vue";
import FavoritesNav from "./Titles/FavoritesNav.vue";
import FavoriteAlbumsNav from "./Titles/FavoriteAlbumsNav.vue";
import FavoriteTracksNav from "./Titles/FavoriteTracksNav.vue";

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
