<template>
  <div class="album-grid-view v-scroll-page">
    <div class="scrollable">
      <AlbumCard
        v-for="album in artist.toShow"
        :album="album"
        :key="album.albumhash"
      />
    </div>
    <!-- <div class="no-albums rounded" v-if="artist.toShow.length == 0">
      <b>No {{ artist.page }}</b>
    </div> -->
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

  .no-albums {
    border: solid $red 1px;
    width: 30rem;
    display: block;
    margin: 0 auto;
    padding: 5rem;
    text-align: center;
    font-size: 1.25rem;
    color: $red;
    opacity: .5;
  }
}
</style>
