<template>
  <QueueActions />
  <div
    class="queue-virtual-scroller"
    style="height: 100%"
    @mouseover="mouseover = true"
    @mouseout="mouseover = false"
  >
    <RecycleScroller
      class="scroller"
      id="queue-scrollable"
      :items="scrollerItems"
      :item-size="itemHeight"
      key-field="id"
      v-slot="{ item, index }"
    >
      <TrackItem
        :track="item.track"
        :isCurrentPlaying="index === queue.currentindex && queue.playing"
        :isCurrent="index === queue.currentindex"
        :isQueueTrack="true"
        @playThis="playFromQueue(index)"
      />
    </RecycleScroller>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

import useQStore from "@/stores/queue";

import TrackItem from "@/components/shared/TrackItem.vue";
import QueueActions from "./Queue/QueueActions.vue";

const itemHeight = 64;
const queue = useQStore();
const mouseover = ref(false);

const scrollerItems = computed(() => {
  return queue.tracklist.map((track) => ({
    id: Math.random(),
    track: track,
  }));
});

function playFromQueue(index: number) {
  queue.play(index);
}

function scrollToCurrent() {
  const elem = document.getElementById("queue-scrollable") as HTMLElement;

  const top = queue.currentindex * itemHeight - itemHeight;
  elem.scroll({
    top,
    behavior: "smooth",
  });
}

onMounted(() => {
  queue.setScrollFunction(scrollToCurrent, mouseover);
});

onBeforeUnmount(() => {
  queue.setScrollFunction(() => {}, null);
});
</script>

<style lang="scss">
.queue-virtual-scroller {
  height: 100%;
  overflow: hidden;

  .scroller {
    height: 100%;
  }
}
</style>
