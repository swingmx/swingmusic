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
import PlaylistCard from "../components/playlists/PlaylistCard.vue";

import usePStore from "../stores/playlists";
import NewPlaylistCard from "../components/playlists/NewPlaylistCard.vue";
const pStore = usePStore();
</script>

<style lang="scss">
#p-view {
  margin: $small;
  padding: $small;
  overflow: auto;
  scrollbar-color: $gray2 transparent;
  border-top: 1px solid $gray3;

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
    gap: $small;
  }
}
</style>
