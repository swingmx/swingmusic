<template>
  <div class="artists-results" v-if="search.artists.value.length">
    <div class="search-results-grid">
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
  display: grid;
  margin: 0 1rem;

  .xartist {
    background-color: $gray;

    .artist-image {
      width: 7rem;
      height: 7rem;
      object-fit: cover;
    }
  }
}
</style>
