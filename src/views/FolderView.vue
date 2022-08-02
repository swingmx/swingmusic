<template>
  <div id="f-view-parent">
    <div id="scrollable" ref="scrollable">
      <div class="banner shadow-lg">
        <div class="text abs rounded pad-medium">
          <h3><FolderSvg /> {{ getFolderName($route) }}</h3>
        </div>
        <img
          src="../assets/images/one.jpg"
          alt="folder page banner"
          class="rounded"
        />
      </div>
      <FolderList :folders="FStore.dirs" v-if="FStore.dirs.length" />
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
  overflow: hidden;

  .h {
    font-size: 2rem;
    font-weight: bold;
  }
}

#scrollable {
  scrollbar-color: grey transparent;
  display: flex;
  flex-direction: column;
  gap: 1rem;

  .banner {
    position: relative;
    height: max-content;
    height: $banner-height;

    .text {
      bottom: 1rem;
      left: 1rem;
      background-color: $black;

      h3 {
        margin: $small;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: $small;
      }
    }

    img {
      height: 100%;
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
