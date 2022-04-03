<template>
  <div class="r-home">
    <UpNext :next="queue.next" :playNext="queue.playNext" />
    <Recommendations />
  </div>
</template>

<style lang="scss">
.r-home {
  height: calc(100% - 1rem);
  padding: 0 $small $small 0;
  margin-top: $small;
}
</style>

<script setup lang="ts">
import Recommendations from "../Recommendation.vue";
import UpNext from "../queue/upNext.vue";
import useQStore from "../../../stores/queue";
const queue = useQStore();
</script>
