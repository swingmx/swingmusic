<template>
  <div class="album-grid-view v-scroll-page">
    <div class="scrollable">
      <AlbumCard v-for="album in albums" :album="album" :key="Math.random()" />
    </div>
  </div>
</template>

<script setup lang="ts">
import useArtistPageStore from "@/stores/pages/artist";
import AlbumCard from "@/components/shared/AlbumCard.vue";
import { getArtistAlbums } from "@/composables/fetch/artists";

import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { Album } from "@/interfaces";

const artist = useArtistPageStore();
const route = useRoute();

const albums = ref(<Album[]>[]);

onMounted(() => {
  // artist.getArtistAlbums(route.params.hash);
  getArtistAlbums(route.params.hash as string).then((res) => {
    albums.value = res.appearances;
    // console.log(albums.value);
  });
});
</script>

<style lang="scss">
.album-grid-view {
  // border: solid;

  .scrollable {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
    grid-gap: $small;
    padding: 0 1rem;
  }
}
</style>
