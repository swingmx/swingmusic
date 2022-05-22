<template>
  <div class="albums-results border">
    <div class="grid">
      <AlbumCard
        v-for="album in search.albums.value"
        :key="album.image"
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

let counter = 0;

function loadMore() {
  counter += 6;
  search.loadAlbums(counter);
}
</script>

<style lang="scss">
.right-search .albums-results {
  border-radius: 0.5rem;
  margin-top: $small;
  padding: $small;
  overflow-x: hidden;

  .result-item:hover {
    background-color: $gray4;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(8rem, 1fr));
    flex-wrap: wrap;
    gap: 0.75rem;
  }
}
</style>
