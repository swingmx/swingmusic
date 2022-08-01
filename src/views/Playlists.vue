<template>
  <div id="p-view">
    <div class="grid">
      <NewPlaylistCard />
      <PlaylistCard
        v-for="p in pStore.playlists"
        :key="p.playlistid"
        :playlist="p"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import PlaylistCard from "@/components/playlists/PlaylistCard.vue";

import usePStore from "@/stores/pages/playlists";
import NewPlaylistCard from "@/components/playlists/NewPlaylistCard.vue";
const pStore = usePStore();
</script>

<style lang="scss">
#p-view {
  overflow: auto;
  scrollbar-color: $gray2 transparent;

  .grid {
    grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
    gap: 1rem;
  }
}
</style>
