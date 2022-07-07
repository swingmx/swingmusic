<template>
  <Page>
    <template #header>
      <Header :album="album.info" />
    </template>
    <template #content>
      <Content :tracks="album.tracks" />
    </template>
    <template #bottom>
      <Bottom :artists="album.artists" :bio="album.bio" />
    </template>
  </Page>
</template>

<script setup lang="ts">
import { onBeforeRouteUpdate, RouteLocationNormalized } from "vue-router";
import useAStore from "@/stores/pages/album";

import Page from "../layouts/HeaderContentBottom.vue";
import Header from "./Header.vue";
import Content from "./Content.vue";
import Bottom from "./Bottom.vue";

const album = useAStore();

onBeforeRouteUpdate(async (to: RouteLocationNormalized) => {
  await album.fetchTracksAndArtists(to.params.hash.toString());
  album.fetchBio(to.params.hash.toString());
});
</script>
