<template>
  <Layout :tracks="album.tracks" @playFromPage="playFromAlbum">
    <template #header>
      <Header :album="album.info" :bio="album.bio" />
    </template>
  </Layout>
</template>

<script setup lang="ts">
import useAStore from "@/stores/pages/album";
import {
  onBeforeRouteLeave,
  onBeforeRouteUpdate,
  RouteLocationNormalized,
} from "vue-router";

import Header from "./Header.vue";
import Layout from "@/layouts/HeaderAndVList.vue";
import useQueueStore from "@/stores/queue";

const album = useAStore();
const queue = useQueueStore();

onBeforeRouteUpdate(async (to: RouteLocationNormalized) => {
  await album
    .fetchTracksAndArtists(to.params.hash.toString())
    .then(() => album.resetQuery());
});

onBeforeRouteLeave(() => {
  setTimeout(() => {
    album.resetQuery();
  }, 500);
});

function playFromAlbum(index: number) {
  const { title, artist, hash } = album.info;
  queue.playFromAlbum(title, artist, hash, album.allTracks);
  queue.play(index);
}
</script>
