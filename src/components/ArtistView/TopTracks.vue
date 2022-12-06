<template>
  <div class="artist-top-tracks">
    <h3 class="section-title">Tracks</h3>
    <div class="tracks">
      <SongItem
        v-for="(song, index) in artist.tracks"
        :track="song"
        :index="index + 1"
      />
    </div>
    <div class="error" v-if="!artist.tracks.length">No tracks</div>
  </div>
</template>

<script setup lang="ts">
import SongItem from "../shared/SongItem.vue";
import useArtistPageStore from "@/stores/pages/artist";

const artist = useArtistPageStore();
</script>

<style lang="scss">
.artist-top-tracks {
  margin-top: 2rem;

  .section-title {
    margin-left: 0;
  }

  .error {
    padding-left: 1rem;
    color: $red;
  }
}
</style>
