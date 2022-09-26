<template>
  <Layout
    :tracks="folder.tracks"
    :no_header="folder.dirs.length === 0"
    @playFromPage="playFromPage"
  >
    <template #header v-if="folder.dirs.length">
      <FolderList :folders="folder.dirs" />
    </template>
  </Layout>
</template>

<script setup lang="ts">
import { onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";

import useQueueStore from "@/stores/queue";
import useLoaderStore from "@/stores/loader";
import useFolderStore from "@/stores/pages/folder";

import Layout from "@/layouts/HeaderAndVList.vue";
import FolderList from "@/components/FolderView/FolderList.vue";

const loader = useLoaderStore();
const folder = useFolderStore();
const queue = useQueueStore();


function playFromPage(index: number) {
  queue.playFromFolder(folder.path, folder.allTracks);
  queue.play(index);
}

onBeforeRouteUpdate((to, from) => {
  loader.startLoading();
  folder
    .fetchAll(to.params.path as string)

    .then(() => {
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
