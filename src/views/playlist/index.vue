<template>
  <Layout :tracks="playlist.tracks" @playFromPage="playFromPlaylistPage">
    <template #header>
      <Header :info="playlist.info" />
    </template>
  </Layout>
</template>

<script setup lang="ts">
import { onBeforeRouteLeave } from "vue-router";

import useQueueStore from "@/stores/queue";
import usePlaylistStore from "@/stores/pages/playlist";

import Layout from "@/layouts/HeaderAndVList.vue";
import Header from "@/components/PlaylistView/Header.vue";

const queue = useQueueStore();
const playlist = usePlaylistStore();

function playFromPlaylistPage(index: number) {
  const { name, playlistid } = playlist.info;
  queue.playFromPlaylist(name, playlistid, playlist.allTracks);
  queue.play(index);
}

onBeforeRouteLeave(() => {
  setTimeout(() => {
    playlist.resetQuery();
  }, 500);
});
</script>
