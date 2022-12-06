<template><div style="height: 1px;"></div></template>

<script setup lang="ts">
import { onMounted } from "vue";
import useArtistPageStore from "@/stores/pages/artist";
import { onBeforeRouteUpdate } from "vue-router";

const store = useArtistPageStore();

onMounted(async () => {
  await store.getArtistAlbums();
});

onBeforeRouteUpdate(async (to) => {
  store.resetAlbums();
  await store.getArtistAlbums();
});
</script>
