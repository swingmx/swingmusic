<template>
  <div class="search-tracks-view">
    <div class="noscroll">
      <Layout :no_header="true" :tracks="search.tracks.value" />
    </div>
    <button @click.prevent="search.loadTracks">Load More</button>
  </div>
</template>

<script setup lang="ts">
import Layout from "@/layouts/HeaderAndVList.vue";
import useSearchStore from "@/stores/search";

const search = useSearchStore();
</script>

<style lang="scss">
.search-tracks-view {
  height: 100%;

  display: grid;
  grid-template-rows: 1fr max-content;
  gap: 1rem;

  button {
    width: fit-content;
    margin: 0 auto;
  }
}
</style>
