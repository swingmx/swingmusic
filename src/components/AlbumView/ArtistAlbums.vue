<template>
  <div class="albums-from-artist">
    <h3>
      <span>More from {{ artist.artist }} </span>
      <span class="see-more">SEE ALL</span>
    </h3>
    <div class="cards">
      <AlbumCard v-for="a in artist.albums" :album="a" />
    </div>
  </div>
</template>

<script setup lang="ts">
import AlbumCard from "../shared/AlbumCard.vue";

import { AlbumInfo } from "@/interfaces";

defineProps<{
  artist: {
    artist: string;
    albums: AlbumInfo[];
  };
}>();
</script>

<style lang="scss">
.albums-from-artist {
  overflow: hidden;
  padding-top: 2rem;

  h3 {
    display: grid;
    grid-template-columns: 1fr max-content;
    align-items: center;
    padding: 0 $medium;

    .see-more {
      font-size: $medium;
    }
  }

  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
    gap: 2rem 0;
  }
}
</style>
