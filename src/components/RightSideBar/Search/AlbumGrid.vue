<template>
  <div class="albums-results">
    <div class="grid">
      <AlbumCard
        v-for="album in search.albums.value"
        :key="`${album.artist}-${album.title}`"
        :album="album"
      />
    </div>
    <LoadMore v-if="search.albums.more" @loadMore="loadMore()" />
  </div>
</template>

<script setup lang="ts">
import AlbumCard from "../../shared/AlbumCard.vue";
import LoadMore from "./LoadMore.vue";
import useSearchStore from "../../../stores/search";

const search = useSearchStore();

function loadMore() {
  search.updateLoadCounter("albums");
  search.loadAlbums(search.loadCounter.albums);
}
</script>

<style lang="scss">
.right-search .albums-results {
  border-radius: 0.5rem;
  overflow-x: hidden;
  margin: 0 1rem;

  .result-item:hover {
    background-color: $gray4;
  }

  .grid {
    grid-template-columns: repeat(auto-fill, minmax(8rem, 1fr));
    flex-wrap: wrap;
    justify-content: flex-start;
    gap: 0.75rem;
  }
}
</style>
