<template>
  <div
    class="artist-albums"
  >
    <h3>
      <span>{{ title }} </span>
      <span class="see-more">SEE ALL</span>
    </h3>
    <div class="cards">
      <AlbumCard v-for="a in albums.slice(0, maxAbumCards)" :album="a" />
    </div>
  </div>
</template>

<script setup lang="ts">
import AlbumCard from "../shared/AlbumCard.vue";
import { Album } from "@/interfaces";

import { maxAbumCards } from "@/stores/content-width";

defineProps<{
  title: string;
  albums: Album[];
}>();
</script>

<style lang="scss">
.artist-albums {
  overflow: hidden;

  h3 {
    display: grid;
    grid-template-columns: 1fr max-content;
    align-items: center;
    padding: 0 $medium;
    margin-bottom: $small;

    .see-more {
      font-size: $medium;
    }
  }

  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
    gap: 5rem 0;
  }
}
</style>
