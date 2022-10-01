<template>
  <div
    class="album_disc_header no-select"
    v-if="album_disc.is_album_disc_number"
  >
    <div class="disc_number">Disc {{ album_disc.album_page_disc_number }}</div>
    <div></div>
  </div>
</template>

<script setup lang="ts">
import { AlbumDisc } from "@/interfaces";

defineProps<{
  album_disc: AlbumDisc;
}>();
</script>

<style lang="scss">
.album_disc_header {
  display: grid;
  grid-template-columns: 1fr max-content;
  align-items: center;
  padding-left: 1rem;
  height: $song-item-height;

  .disc_number {
    font-size: $medium;
    opacity: 0.75;
  }
}
</style>
