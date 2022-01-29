<template>
  <div class="r-sidebar">
    <!-- <div class="m-np"> -->
      <!-- <NowPlaying class="hidden"/> -->
    <!-- </div> -->
    <div class="s">
      <Search
        v-model:search="search"
        @expandSearch="expandSearch"
        @collapseSearch="collapseSearch"
      />
    </div>
    <div class="q">
      <UpNext v-model:up_next="up_next" @expandQueue="expandQueue" />
    </div>
    <div class="r">
      <RecommendedArtist />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Search from "../Search.vue";
import UpNext from "./UpNext.vue";
import RecommendedArtist from "@/components/RightSideBar/Recommendation.vue";

let up_next = ref(true);
let search = ref(false);

const expandQueue = () => {
  up_next.value = !up_next.value;
};

const expandSearch = () => {
  search.value = true;
};

const collapseSearch = () => {
  search.value = false;
};
</script>

<style lang="scss">
.r-sidebar {
  border-radius: 5px;
  margin-right: 0.5rem;
  margin-bottom: $small;
  overflow-y: auto;
  width: 30em;
  display: grid;
  grid-auto-flow: row;
  grid-template-rows: min-content min-content auto;
}
</style>
