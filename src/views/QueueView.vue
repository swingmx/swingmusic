<template>
  <div class="queue-view">
    <SongList :tracks="queue.tracklist" @playFromPage="playFromQueuePage" />
  </div>
</template>

<script setup lang="ts">
import useQStore from "@/stores/queue";
import { focusElem } from "@/utils";
import SongList from "@/components/FolderView/SongList.vue";
import { onMounted } from "vue";

const queue = useQStore();

function playFromQueuePage(index: number) {
  queue.play(index);
}

onMounted(() => {
  setTimeout(() => {
    focusElem("current");
  }, 1000);
});
</script>

<!-- <style lang="scss">
.queue-view {
  .table {
    margin-top: -1rem;
  }
}
</style> -->
