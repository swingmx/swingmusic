<template>
  <div id="f-view-parent">
    <div id="scrollable" ref="scrollable">
      <div class="banner shadow-lg rounded">
        <div class="text abs rounded pad-medium">
          <h3><FolderSvg /> {{ getFolderName($route) }}</h3>
        </div>
        <img
          src="@/assets/images/folderbg.webp"
          alt=""
          class="rounded"
          loading="lazy"
        />
      </div>
      <FolderList :folders="folder.dirs" v-if="folder.dirs.length" />
      <SongList
        :tracks="folder.tracks"
        :path="folder.path"
        @playFromPage="playFromPage"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "@vue/reactivity";
import {
  onBeforeRouteLeave,
  onBeforeRouteUpdate,
  RouteLocationNormalized,
} from "vue-router";

import SongList from "@/components/FolderView/SongList.vue";
import FolderList from "@/components/FolderView/FolderList.vue";
import FolderSvg from "@/assets/icons/folder.svg";

import useFolderStore from "@/stores/pages/folder";
import useQueueStore from "@/stores/queue";
import useLoaderStore from "@/stores/loader";
import { isSameRoute } from "@/composables/perks";

const loader = useLoaderStore();
const folder = useFolderStore();
const queue = useQueueStore();

const scrollable = ref<any>(null);

function getFolderName(route: RouteLocationNormalized) {
  const path = route.params.path as string;
  return path.split("/").pop();
}

function playFromPage(index: number) {
  queue.playFromFolder(folder.path, folder.allTracks);
  queue.play(index);
}

onBeforeRouteUpdate((to, from) => {
  loader.startLoading();
  folder
    .fetchAll(to.params.path as string)

    .then(() => {
      scrollable.value.scrollTop = 0;
      folder.resetQuery();
    })
    .then(() => {
      loader.stopLoading();
    });
});

onBeforeRouteLeave(() => {
  setTimeout(() => folder.resetQuery(), 500);
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
    pointer-events: none;
    user-select: none;
    width: 100%;
    background-color: $accent;

    .text {
      bottom: 1rem;
      left: 1rem;
      width: max-content;
      max-width: calc(100% - 2rem);
      background-color: $black;

      @include for-desktop-down {
        right: 1rem;
      }

      h3 {
        margin: $small;
        display: grid;
        grid-template-columns: max-content 1fr;
        align-items: center;
        justify-content: center;
        gap: $small;
      }
    }

    img {
      height: 100%;
      width: 100%;
      object-fit: cover;
      object-position: bottom right;
      transition: all 0.25s ease;
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
