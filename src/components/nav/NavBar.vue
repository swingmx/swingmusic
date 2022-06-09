<template>
  <div class="topnav">
    <div class="left">
      <div class="btn">
        <NavButtons />
      </div>

      <div class="info">
        <Album v-show="$route.name == Routes.album && !nav.showPlay" />
        <Playlists v-show="$route.name == Routes.playlists" />
        <Folder v-show="$route.name == Routes.folder" :subPaths="subPaths" />
      </div>
    </div>

    <div class="center rounded">
      <Loader />
    </div>
    <div class="right">
      <div class="more image"></div>
      <Search />
    </div>
  </div>
</template>

<script setup lang="ts">
import NavButtons from "./NavButtons.vue";
import Loader from "../shared/Loader.vue";
import Search from "./Search.vue";
import { useRoute } from "vue-router";
import { onMounted, ref, watch } from "vue";
import { Routes } from "@/composables/enums";
import createSubPaths from "@/composables/createSubPaths";
import { subPath } from "@/interfaces";
import Folder from "./Titles/Folder.vue";
import Playlists from "./Titles/Playlists.vue";
import Album from "./Titles/Album.vue";
import useNavStore from "@/stores/nav";

const route = useRoute();
const nav = useNavStore();

const subPaths = ref<subPath[]>([]);

function useSubRoutes() {
  watch(
    () => route.name,
    (newRoute: string) => {
      switch (newRoute) {
        case Routes.folder:
          let oldpath = "";
          [oldpath, subPaths.value] = createSubPaths(
            route.params.path,
            oldpath
          );

          watch(
            () => route.params.path,
            (newPath) => {
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
}

onMounted(() => {
  useSubRoutes();
});
</script>

<style lang="scss">
.topnav {
  display: grid;
  grid-template-columns: 1fr min-content max-content;
  padding-bottom: 1rem;
  margin: $small $small 0 0;
  border-bottom: 1px solid $gray3;
  height: 3rem;

  .left {
    display: grid;
    grid-template-columns: max-content 1fr;

    .info {
      min-width: 15rem;

      .title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: $smaller;
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

    .more {
      width: 2.25rem;
      aspect-ratio: 1;
      height: 100%;
      background-color: $gray5;
      background-image: url("../../assets/icons/more.svg");
      transform: rotate(90deg);
      border-radius: $small;
    }
  }
}
</style>
