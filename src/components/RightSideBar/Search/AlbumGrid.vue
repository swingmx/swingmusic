<template>
  <div class="artists-results">
    <div class="search-results-grid">
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
