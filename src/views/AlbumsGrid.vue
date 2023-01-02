<template>
  <div class="card-grid-view v-scroll-page">
    <div class="scrollable">
      <AlbumCard
        v-for="album in artist.toShow"
        :album="album"
        :key="album.albumhash"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import AlbumCard from "@/components/shared/AlbumCard.vue";
import useArtistDiscographyStore from "@/stores/pages/artistDiscog";

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