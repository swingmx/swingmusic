<template>
  <SongList :tracks="queue.tracklist" :handlePlay="playFromQueue" />
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import useQStore from "@/stores/queue";
import SongList from "@/components/shared/SongList.vue";

const queue = useQStore();
function playFromQueue(index: number) {
  queue.play(index);
}

function scrollToCurrent() {
  const scrollable = document.getElementById("songlist-scroller");
  const itemHeight = 64;
  const top = (queue.currentindex - 1) * itemHeight;

  scrollable?.scrollTo({
    top,
    behavior: "smooth",
  });
}

onMounted(() => {
  setTimeout(() => {
    scrollToCurrent();
  }, 1000);
});
</script>

<style lang="scss">
.queue-view-virtual-scroller {
  .songlist-item.current {
    background-color: $darkestblue !important;
  }
}
</style>
