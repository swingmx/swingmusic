<template>
  <div class="grid-page">
    <ArtistCard
      v-for="artist in search.artists.value"
      :key="artist.image"
      :artist="artist"
    />
  </div>
</template>

<script setup lang="ts">
import ArtistCard from "@/components/shared/ArtistCard.vue";
import useSearchStore from "@/stores/search";

const search = useSearchStore();
</script>