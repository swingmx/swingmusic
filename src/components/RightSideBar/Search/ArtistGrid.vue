<template>
  <div class="artists-results">
    <div
      class="search-results-grid"
      v-if="album_grid == true && search.albums.value.length"
    >
      <AlbumCard v-for="a in search.albums.value" :key="a.albumid" :album="a" />
    </div>
    <div
      class="search-results-grid"
      v-else-if="!album_grid && search.artists.value.length"
    >
      <ArtistCard
        v-for="artist in search.artists.value"
        :key="artist.image"
        :artist="artist"
        :alt="true"
      />
    </div>
    <div v-else class="t-center"><h5>🤷</h5></div>
    <LoadMore
      v-if="album_grid && search.albums.more"
      :loader="search.loadAlbums"
    />
    <LoadMore
      v-if="!album_grid && search.artists.more"
      :loader="search.loadArtists"
    />
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
</script>

<style lang="scss">
.artists-results {
  display: grid;
  margin: 0 1rem;
}

.search-results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
  gap: 0.75rem;
}
</style>
