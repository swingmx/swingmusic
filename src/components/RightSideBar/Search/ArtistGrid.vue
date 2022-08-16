<template>
  <div class="artists-results">
    <div class="search-results-grid" v-if="album_grid == true">
      <AlbumCard v-for="a in search.albums.value" :key="a.albumid" :album="a" />
    </div>
    <div class="search-results-grid" v-else>
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

import AlbumCard from "@/components/shared/AlbumCard.vue";
import ArtistCard from "../../shared/ArtistCard.vue";
import LoadMore from "./LoadMore.vue";

const search = useSearchStore();

defineProps<{
  album_grid?: boolean;
}>();

function loadMore() {
  search.updateLoadCounter("artists");
  search.loadArtists(search.loadCounter.artists);
}
</script>

<style lang="scss">
.artists-results {
  display: grid;
  margin: 0 1rem;
}

.search-results-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}
</style>
