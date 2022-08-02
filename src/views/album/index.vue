<template>
  <Page :bottomRaisedCallback="fetchAlbumBio">
    <template #header>
      <Header :album="album.info" />
    </template>
    <template #content>
      <Content :discs="discs" />
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
import { Track } from "@/interfaces";
import { ref } from "vue";

const album = useAStore();

// function that takes in a Track[] and returns a Track[][] which is a list of tracks split into discs
interface Disc {
  [key: string]: Track[];
}

function createDiscs(tracks: Track[]): Disc {
  // group tracks by disc using array.reduce
  return tracks.reduce((group, track) => {
    const { discnumber } = track;
    group[discnumber] = group[discnumber] ?? [];
    group[discnumber].push(track);
    return group;
  }, {} as Disc);
}

const discs = ref(createDiscs(album.tracks));

console.log(discs.value);
function fetchAlbumBio(params: RouteParams) {
  album.fetchBio(params.hash.toString());
}

onBeforeRouteUpdate(async (to: RouteLocationNormalized) => {
  await album.fetchTracksAndArtists(to.params.hash.toString()).then(() => {
    discs.value = createDiscs(album.tracks);
  });
});
</script>
