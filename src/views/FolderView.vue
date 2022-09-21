<template>
  <Layout :tracks="folder.tracks" @playFromPage="playFromPage">
    <template #header>
      <FolderList :folders="folder.dirs" v-if="folder.dirs.length" />
    </template>
  </Layout>
</template>

<script setup lang="ts">
import { ref } from "@vue/reactivity";
import { onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";

import useQueueStore from "@/stores/queue";
import useLoaderStore from "@/stores/loader";
import useFolderStore from "@/stores/pages/folder";

import Layout from "@/layouts/HeaderAndVList.vue";
import SongList from "@/components/FolderView/SongList.vue";
import FolderList from "@/components/FolderView/FolderList.vue";

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
