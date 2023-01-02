<template>
  <div class="card-grid-view v-scroll-page">
    <div class="scrollable">
      <ArtistCard
        v-for="artist in artists"
        :artist="artist"
        :key="artist.artisthash"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { getFavArtists } from "@/composables/fetch/favorite";
import { onMounted, Ref, ref } from "vue";

import ArtistCard from "@/components/shared/ArtistCard.vue";
import { Artist } from "@/interfaces";

const artists: Ref<Artist[]> = ref([]);

onMounted(() => {
  getFavArtists(0).then((data) => (artists.value = data));
});
</script>
