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
  background-color: $black;
  padding-top: 0;

  .scrollable {
    height: 100%;
    overflow: auto;
  }
}
</style>
