<template>
  <div class="topnav">
    <div class="left">
      <div class="btn">
        <NavButtons />
      </div>

      <div class="info">
        <div
          class="title"
          v-show="$route.name == 'Playlists'"
          v-motion
          :initial="{
            opacity: 0,
            x: -20,
          }"
          :visible="{
            opacity: 1,
            x: 0,
            transition: {
              delay: 100,
            },
          }"
        >
          Playlists
        </div>
        <Folder :subPaths="subPaths" />
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

const route = useRoute();

const subPaths = ref<subPath[]>([]);

function useSubRoutes() {
  watch(
    () => route.name,
    (newRoute: string) => {
      switch (newRoute) {
        case Routes.folder:
          console.log(newRoute);
          subPaths.value = createSubPaths(route.params.path);

          watch(
            () => route.params.path,
            (newPath) => {
              if (newPath == undefined) return;

              subPaths.value = createSubPaths(newPath);
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
