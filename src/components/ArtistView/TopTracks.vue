<template>
  <div class="artist-top-tracks">
    <h3 class="section-title">Tracks</h3>
    <div class="tracks">
      <SongItem
        v-for="(song, index) in artist.tracks"
        :track="song"
        :index="index + 1"
        :isCurrent="false"
        :isCurrentPlaying="false"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import useQueueStore from "@/stores/queue";
import SongItem from "../shared/SongItem.vue";
import useArtistPageStore from "@/stores/pages/artist";

const queue = useQueueStore();
const artist = useArtistPageStore();
</script>

<style lang="scss">
.artist-top-tracks {
  // padding-bottom: 2rem;

  .section-title {
    margin-left: 0;
  }
}
</style>
