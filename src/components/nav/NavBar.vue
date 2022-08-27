<template>
  <div class="topnav">
    <div class="left">
      <NavButtons />
      <div
        class="info"
        :style="{
          overflow: $route.name === Routes.search ? 'visible' : 'hidden',
        }"
      >
        <APTitle v-if="showAPTitle" />
        <SimpleTitle
          v-if="$route.name == Routes.playlists"
          :text="'Playlists'"
        />
        <SimpleTitle v-if="$route.name == Routes.settings" :text="'Settings'" />
        <Folder v-if="$route.name == Routes.folder" :subPaths="subPaths" />
        <SearchTitle v-if="$route.name == Routes.search" />
      </div>
    </div>

    <div class="center rounded">
      <Loader />
    </div>
  </div>
</template>

<script setup lang="ts">
import NavButtons from "./NavButtons.vue";
import Loader from "../shared/Loader.vue";
import { useRoute } from "vue-router";
import { ref, watch } from "vue";
import { Routes } from "@/composables/enums";
import { createSubPaths } from "@/utils";
import { subPath } from "@/interfaces";
import Folder from "./Titles/Folder.vue";
import SimpleTitle from "./Titles/SimpleTitle.vue";
import APTitle from "./Titles/APTitle.vue";
import useNavStore from "@/stores/nav";

import { computed } from "@vue/reactivity";
import SearchTitle from "./Titles/SearchTitle.vue";

const route = useRoute();
const nav = useNavStore();

const subPaths = ref<subPath[]>([]);

const showAPTitle = computed(() => {
  return (
    (route.name == Routes.album || route.name == Routes.playlist) &&
    !nav.h_visible
  );
});

watch(
  () => route.name,
  (newRoute: string) => {
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
  gap: $small;

  .left {
    display: grid;
    grid-template-columns: max-content 1fr;
    gap: 1rem;

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
