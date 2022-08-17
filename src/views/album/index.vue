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
import {
  onBeforeRouteUpdate,
  RouteLocationNormalized,
  RouteParams,
} from "vue-router";

import Page from "@/layouts/HeaderContentBottom.vue";
import Content from "./Content.vue";
import Header from "./Header.vue";

const album = useAStore();

function fetchAlbumBio(params: RouteParams) {
  album.fetchBio(params.hash.toString());
}

onBeforeRouteUpdate(async (to: RouteLocationNormalized) => {
  await album
    .fetchTracksAndArtists(to.params.hash.toString())
    .then(() => album.fetchBio(to.params.hash.toString()));
});
</script>
