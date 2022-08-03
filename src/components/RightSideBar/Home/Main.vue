<template>
  <div class="r-home">
    <UpNext :next="queue.tracks[queue.next]" :playNext="queue.playNext" />
    <Recommendations />
  </div>
</template>

<style lang="scss">
.r-home {
  height: calc(100% - 1rem);
}
</style>

<script setup lang="ts">
import Recommendations from "./Recommendation.vue";
import UpNext from "../Queue/upNext.vue";
import useQStore from "../../../stores/queue";
const queue = useQStore();
</script>
