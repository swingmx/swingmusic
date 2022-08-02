<template>
  <div class="topnav">
    <div class="left">
      <div class="btn">
        <NavButtons />
      </div>

      <div class="info">
        <APTitle v-show="showAPTitle" />
        <Playlists v-show="$route.name == Routes.playlists" />
        <Folder v-show="$route.name == Routes.folder" :subPaths="subPaths" />
      </div>
    </div>

    <div class="center rounded">
      <Loader />
    </div>
    <div class="right">
      <Search />
    </div>
  </div>
</template>

<script setup lang="ts">
import NavButtons from "./NavButtons.vue";
import Loader from "../shared/Loader.vue";
import Search from "./Search.vue";
import { useRoute } from "vue-router";
import { ref, watch } from "vue";
import { Routes } from "@/composables/enums";
import createSubPaths from "@/composables/createSubPaths";
import { subPath } from "@/interfaces";
import Folder from "./Titles/Folder.vue";
import Playlists from "./Titles/Playlists.vue";
import APTitle from "./Titles/APTitle.vue";
import useNavStore from "@/stores/nav";

import { computed } from "@vue/reactivity";

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
  grid-template-columns: 1fr min-content max-content;

  .left {
    display: grid;
    grid-template-columns: max-content 1fr;

    .info {
      min-width: 15rem;

      .title {
        font-size: 1.5rem;
        font-weight: bold;
        display: flex;
      }
    }
  }

  .center {
    display: grid;
    place-items: center;
    margin-right: 1rem;
  }

  .right {
    width: 100%;
    display: flex;
    gap: $small;
  }
}
</style>
