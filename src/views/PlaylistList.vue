<template>
  <div id="p-view" class="content-page">
    <div class="grid">
      <PlaylistCard v-for="p in pStore.playlists" :key="p.id" :playlist="p" />
    </div>
  </div>
</template>

<script setup lang="ts">
import PlaylistCard from "@/components/PlaylistsList/PlaylistCard.vue";

import usePStore from "@/stores/pages/playlists";
const pStore = usePStore();

// TODO: When you add a song to playlist when you are in this page, increase the count on the card.
</script>

<style lang="scss">
#p-view {
  padding-bottom: $content-padding-bottom;
  height: 100%;
  overflow: auto;
  padding-right: 1rem;

  .grid {
    grid-template-columns: repeat(auto-fill, minmax(9.25rem, 1fr));
    gap: 2.5rem 1.75rem;
  }
}
</style>
