<template>
  <div class="search-view">
    <div class="tabs">
      <button v-for="page in pages">{{ page }}</button>
    </div>
    <div class="noscroll">
      <component :is="getComponent()" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";

import TracksPage from "./tracks.vue";
import AlbumPage from "./albums.vue";
import ArtistPage from "./artists.vue";

enum pages {
  tracks = "tracks",
  albums = "albums",
  artists = "artists",
}

const route = useRoute();
const page = route.params.page as string;

function getComponent() {
  switch (page) {
    case pages.tracks:
      return TracksPage;
    case pages.albums:
      return AlbumPage;

    case pages.artists:
      return ArtistPage;

    default:
      return TracksPage;
  }
}
</script>

<style lang="scss">
.search-view {
  height: calc(100% - 1rem);
  width: calc(100% - $small);
  display: grid;
  grid-template-rows: max-content 1fr;

  .tabs {
    width: fit-content;
    display: flex;
    gap: 1rem;
    // margin: 0 auto;
    margin-bottom: 1rem;

    & > * {
      background-color: $gray4;
      padding: $small 1rem;
      border-radius: $small;
      text-transform: capitalize;
    }
  }
}
</style>
