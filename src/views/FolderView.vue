<template>
  <div id="f-view-parent">
    <div id="scrollable" ref="scrollable">
      <div class="banner shadow-lg">
        <div class="text abs rounded pad-medium">
          <h1><FolderSvg /> {{ getFolderName($route) }}</h1>
        </div>
        <img src="../assets/images/one.jpg" alt="" class="rounded" />
      </div>
      <FolderList :folders="FStore.dirs" />
      <SongList :tracks="FStore.tracks" :path="FStore.path" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "@vue/reactivity";
import { onBeforeRouteUpdate, RouteLocationNormalized } from "vue-router";

import SongList from "@/components/FolderView/SongList.vue";
import FolderList from "@/components/FolderView/FolderList.vue";
import FolderSvg from "@/assets/icons/folder.svg";

import useFStore from "../stores/pages/folder";
import useLoaderStore from "../stores/loader";
import { isSameRoute } from "@/composables/perks";

const loader = useLoaderStore();
const FStore = useFStore();

const scrollable = ref(null);

function getFolderName(route: RouteLocationNormalized) {
  const path = route.params.path as string;
  return path.split("/").pop();
}

onBeforeRouteUpdate((to, from) => {
  if (isSameRoute(to, from)) return;

  loader.startLoading();
  FStore.fetchAll(to.params.path as string)

    .then(() => {
      console.log("fetched");
      scrollable.value.scrollTop = 0;
    })
    .then(() => {
      loader.stopLoading();
    });
});
</script>

<style lang="scss">
#f-view-parent {
  position: relative;

  .h {
    font-size: 2rem;
    font-weight: bold;
  }
}

#scrollable {
  overflow-y: auto;
  height: calc(100% - $small);
  scrollbar-color: grey transparent;

  .banner {
    margin-bottom: $small;
    position: relative;

    svg {
      transform: scale(1.5);
    }

    .text {
      bottom: 1rem;
      left: 1rem;
      background-color: $black;

      h1 {
        margin: $small;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: $small;
      }
    }

    img {
      height: $banner-height;
      width: 100%;
      object-fit: cover;
    }
  }

  @include phone-only {
    padding-right: 0;

    &::-webkit-scrollbar {
      display: none;
    }
  }
}
</style>
