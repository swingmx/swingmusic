<template>
  <div id="f-view-parent">
    <div id="scrollable" ref="scrollable">
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
} from "vue-router";

import SongList from "@/components/FolderView/SongList.vue";
import FolderList from "@/components/FolderView/FolderList.vue";

import useFolderStore from "@/stores/pages/folder";
import useQueueStore from "@/stores/queue";
import useLoaderStore from "@/stores/loader";

const loader = useLoaderStore();
const folder = useFolderStore();
const queue = useQueueStore();

const scrollable = ref<any>(null);

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
}

#scrollable {
  display: grid;
  gap: 1rem;
}
</style>
