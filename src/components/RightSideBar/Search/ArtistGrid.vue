<template>
  <div class="artists-results bg-black">
    <div class="grid">
      <ArtistCard
        v-for="artist in search.artists.value"
        :key="artist.image"
        :artist="artist"
        :alt="true"
      />
    </div>
    <LoadMore v-if="search.artists.more" @loadMore="loadMore" />
  </div>
</template>

<script setup lang="ts">
import useSearchStore from "../../../stores/search";
import ArtistCard from "../../shared/ArtistCard.vue";
import LoadMore from "./LoadMore.vue";
const search = useSearchStore();

function loadMore() {
  search.updateLoadCounter("artists");
  search.loadArtists(search.loadCounter.artists);
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
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
  }
}
</style>
