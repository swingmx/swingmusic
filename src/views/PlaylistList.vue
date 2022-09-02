<template>
  <div id="p-view">
    <div class="grid">
      <!-- <NewPlaylistCard /> -->
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

import NewPlaylistCard from "@/components/PlaylistsList/NewPlaylistCard.vue";
import usePStore from "@/stores/pages/playlists";
const pStore = usePStore();
</script>

<style lang="scss">
#p-view {
  overflow: auto;
  scrollbar-color: $gray2 transparent;

  .grid {
    grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr));
    gap: 1rem;

    // @include for-desktop-down {
    //   grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));

    //   .name {
    //     font-size: 0.9rem;
    //   }
    // }
  }
}
</style>
