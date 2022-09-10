<template>
  <Page>
    <template #header>
      <Header :album="album.info" :bio="album.bio" />
    </template>
    <template #content>
      <Content :discs="album.discs" :copyright="album.info.copyright" />
    </template>
  </Page>
</template>

<script setup lang="ts">
import useAStore from "@/stores/pages/album";
import { onBeforeRouteUpdate, RouteLocationNormalized } from "vue-router";

import Header from "./Header.vue";
import Content from "./Content.vue";
import Page from "@/layouts/HeaderContentBottom.vue";

const album = useAStore();

onBeforeRouteUpdate(async (to: RouteLocationNormalized) => {
  await album
    .fetchTracksAndArtists(to.params.hash.toString())
    .then(() => album.fetchBio(to.params.hash.toString()));
});
</script>
