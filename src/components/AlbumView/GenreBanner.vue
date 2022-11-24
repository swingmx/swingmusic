<template>
  <div class="genres-banner">
    <div v-for="genre in genres" class="rounded pad-sm">{{ genre }}</div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import useAlbumStore from "@/stores/pages/album";

const genres = ["Genres", "RNB", "Alternative", "Genres", "RNB", "Alternative"];

onMounted(() => {
  // onMounted, fetch data to be used in the component below this one.
  const album = useAlbumStore();
  album.fetchArtistAlbums();
});
</script>

<style lang="scss">
.genres-banner {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  font-size: 0.9rem;
  padding-left: $medium;
  text-transform: capitalize;
  user-select: none;

  div {
    background-color: $gray5;
    min-width: 4rem;
    text-align: center;
    outline: solid 1px $gray3;
    padding: $small 1rem;

    &:first-child {
      background-color: white;
      color: black;
      outline-color: white;
      pointer-events: none;
    }

    &:hover {
      background-color: $darkestblue;
      outline-color: $darkestblue;
    }
  }
}
</style>
