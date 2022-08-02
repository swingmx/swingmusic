<template>
  <div class="albums-results bg-black">
    <div class="grid">
      <PCard
        v-for="album in search.albums.value"
        :key="`${album.artist}-${album.title}`"
        :album="album"
      />
    </div>
    <LoadMore v-if="search.albums.more" @loadMore="loadMore()" />
  </div>
</template>

<script setup lang="ts">
import useSearchStore from "../../../stores/search";
import PCard from "../../playlists/PlaylistCard.vue";
import LoadMore from "./LoadMore.vue";

const search = useSearchStore();

function loadMore() {
  search.updateLoadCounter("albums");
  search.loadAlbums(search.loadCounter.albums);
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
    grid-template-columns: repeat(auto-fill, minmax(8rem, 1fr));
    flex-wrap: wrap;
    gap: 0.75rem;
  }
}
</style>
