<template>
  <Page :bottomRaisedCallback="fetchAlbumBio">
    <template #header>
      <Header :album="album.info" />
    </template>
    <template #content>
      <Content :discs="album.discs" :copyright="album.info.copyright" />
    </template>
    <template #bottom>
      <Bottom
        :artists="album.artists"
        :bio="album.bio"
        :image="album.info.image"
      />
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
import Bottom from "./Bottom.vue";
import Content from "./Content.vue";
import Header from "./Header.vue";

const album = useAStore();

function fetchAlbumBio(params: RouteParams) {
  album.fetchBio(params.hash.toString());
}

onBeforeRouteUpdate(async (to: RouteLocationNormalized) => {
  await album.fetchTracksAndArtists(to.params.hash.toString());
});
</script>
