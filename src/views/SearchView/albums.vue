<template>
  <div class="search-albums-view grid-page" v-auto-animate>
    <AlbumCard
      v-for="album in search.albums.value"
      :key="album.albumhash"
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
// .search-albums-view.grid-page {
//   max-height: 100%;
//   display: grid;
//   grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr));
//   gap: 1.75rem 0;

//   padding-bottom: 4rem;
//   padding-right: $medium;

//   overflow: auto;
// }
</style>
