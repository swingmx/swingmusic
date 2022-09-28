<template>
  <div class="search-view">
    <div class="scrollable">
      <Main :isOnSearchPage="true" />
    </div>
  </div>
</template>

<script setup lang="ts">
import Main from "@/components/RightSideBar/Search/Main.vue";
</script>

<style lang="scss">
.search-view {
  height: 100%;
  padding-top: 0;
  margin-right: -1rem;

  .scrollable {
    height: 100%;
    overflow: auto;
  }

  .artists-results {
    margin-right: calc($medium + 1px);
    margin-left: 0;
  }

  .search-results-grid {
    grid-template-columns: repeat(auto-fill, minmax(11rem, 1fr));

    .artist-card {
      padding: 0 1rem;
    }
  }

  #tracks-results {
    margin-right: 1rem;
  }
}
</style>
