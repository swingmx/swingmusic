<template>
  <div class="search-albums-view grid-page">
    <AlbumCard
      v-for="album in search.albums.value"
      :key="Math.random()"
      :album="album"
    />
  </div>
</template>

<script setup lang="ts">
import AlbumCard from "@/components/shared/AlbumCard.vue";
import useSearchStore from "@/stores/search";

const search = useSearchStore();
</script>

<style lang="scss">
.search-albums-view.grid-page {
  padding-right: $small;

  overflow: auto;
}
</style>
