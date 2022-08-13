<template>
  <div class="r-home">
    <UpNext :track="queue.tracklist[queue.next]" :playNext="queue.playNext" />
    <!-- <Recommendations /> -->
  </div>
</template>

<style lang="scss">
.r-home {
  height: calc(100% - 1rem);
}
</style>

<script setup lang="ts">
import useQStore from "../../../stores/queue";
import UpNext from "../Queue/upNext.vue";
const queue = useQStore();
</script>
