<template>
  <div class="search-tracks-view">
    <div class="no-scroll">
      <Layout
        :no_header="true"
        :tracks="search.tracks.value"
        @playFromPage="playFromSearch"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import Layout from "@/layouts/HeaderAndVList.vue";
import useSearchStore from "@/stores/search";
import useQueueStore from "@/stores/queue";

const search = useSearchStore();
const queue = useQueueStore();

function playFromSearch(index: number) {
  queue.playFromSearch(search.query, search.tracks.value);
  queue.play(index);
}
</script>

<style lang="scss">
.search-tracks-view {
  height: 100%;

  .no-scroll {
    height: 100%;
  }

  .header-list-layout {
    width: 100%;
  }

  button {
    width: fit-content;
    margin: 0 auto;
  }
}
</style>
