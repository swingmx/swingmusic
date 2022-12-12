<template>
  <div class="album-grid-view v-scroll-page">
    <div class="scrollable" v-auto-animate="{ duration: 100 }">
      <AlbumCard
        v-for="album in artist.toShow"
        :album="album"
        :key="album.albumhash"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import useArtistDiscographyStore from "@/stores/pages/artistDiscog";
import AlbumCard from "@/components/shared/AlbumCard.vue";

import { onMounted } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";

const artist = useArtistDiscographyStore();
const route = useRoute();

onMounted(() => {
  artist.fetchAlbums(route.params.hash as string);
});

onBeforeRouteLeave(() => {
  artist.resetAlbums();
});
</script>

<style lang="scss">
.album-grid-view {
  height: 100%;

  .scrollable {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
    grid-gap: $small;
    padding: 0 1rem;
    padding-bottom: 4rem;
    overflow: auto;
    max-height: 100%;
  }
}
</style>
