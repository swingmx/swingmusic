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
  // background-color: $black;
  padding-top: 0;
  margin-right: -1rem;

  .scrollable {
    height: 100%;
    overflow: auto;
  }

  .search-results-grid {
    grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
  }
}
</style>
