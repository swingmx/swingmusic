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
import PlaylistCard from "../components/playlists/PlaylistCard.vue";

import usePStore from "../stores/playlists";
const pStore = usePStore();
</script>

<style lang="scss">
#p-view {
  margin: $small;
  padding: $small;
  overflow: auto;

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(9rem, 1fr));
    gap: 1rem;
  }
}
</style>
