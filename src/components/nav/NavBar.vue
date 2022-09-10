<template>
  <div class="topnav">
    <div class="left">
      <NavButtons />

      <div
        :style="{
          overflowY: hideOverflow() ? 'visible' : 'hidden',
        }"
        class="info"
      >
        <APTitle
          v-if="$route.name == Routes.album || $route.name == Routes.playlist"
          :header_shown="nav.h_visible"
        />
        <SettingsTitle v-if="$route.name == Routes.settings" :text="'Settings'" />
        <FolderTitle v-if="$route.name == Routes.folder" :subPaths="subPaths" />
        <SearchTitle v-if="$route.name == Routes.search" />
        <PlaylistsTitle v-if="$route.name == Routes.playlists" />
        <QueueTitle v-if="$route.name == Routes.queue" />
      </div>
    </div>
    <!-- 
    <div class="center rounded">
      <Loader />
    </div> -->
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

import { subPath } from "@/interfaces";
import useNavStore from "@/stores/nav";
import { createSubPaths } from "@/utils";
import { Routes } from "@/composables/enums";

import NavButtons from "./NavButtons.vue";

import FolderTitle from "./Titles/Folder.vue";
import SimpleTitle from "./Titles/SimpleTitle.vue";
import APTitle from "./Titles/APTitle.vue";
import SearchTitle from "./Titles/SearchTitle.vue";
import PlaylistsTitle from "./Titles/PlaylistsTitle.vue";
import QueueTitle from "./Titles/QueueTitle.vue";
import SettingsTitle from "./Titles/SettingsTitle.vue";

const route = useRoute();
const nav = useNavStore();

const subPaths = ref<subPath[]>([]);

function hideOverflow() {
  const { name } = route;
  const { album, playlist, search, folder } = Routes;

  return (album + playlist + search + folder).includes(name as string);
}

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
