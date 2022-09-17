<template>
  <div id="p-view">
    <div class="grid">
      <PlaylistCard
        v-for="p in pStore.playlists"
        :key="p.playlistid"
        :playlist="p"
      />
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
  scrollbar-color: $gray2 transparent;

  .grid {
    grid-template-columns: repeat(auto-fill, minmax(11rem, 1fr));
    gap: 1rem;
  }
}
</style>
