<template>
  <div class="artists-results border">
    <div class="grid">
      <ArtistCard
        v-for="artist in search.artists.value"
        :key="artist.image"
        :artist="artist"
      />
    </div>
    <LoadMore v-if="search.artists.more" @loadMore="loadMore" />
  </div>
</template>

<script setup lang="ts">
import ArtistCard from "../../shared/ArtistCard.vue";
import LoadMore from "./LoadMore.vue";
import useSearchStore from "../../../stores/search";
const search = useSearchStore();

let counter = 0;

function loadMore() {
  counter += 6;
  search.loadArtists(counter);
}
</script>

<style lang="scss">
.right-search .artists-results {
  border-radius: 0.5rem;
  padding: $small;
  margin-bottom: $small;


  .xartist {
    background-color: $gray;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
  }
}
</style>
