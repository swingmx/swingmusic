<template>
  <div class="search-tracks-view">
    <div class="no-scroll">
      <Layout :no_header="true" :tracks="search.tracks.value" />
    </div>
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
