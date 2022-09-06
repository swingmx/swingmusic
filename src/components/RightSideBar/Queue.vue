<template>
  <QueueActions />
  <div
    class="scrollable-r"
    @mouseover="mouseover = true"
    @mouseout="mouseover = false"
  >
    <div class="inner">
      <TrackItem
        v-for="(t, index) in queue.tracklist"
        :key="index"
        :track="t"
        :index="index + 1"
        :isPlaying="queue.playing"
        :isHighlighted="false"
        :isCurrent="index === queue.currentindex"
        @PlayThis="playFromQueue(index)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onUpdated, ref } from "vue";

import useQStore from "@/stores/queue";
import { focusElem } from "@/utils";

import TrackItem from "../shared/TrackItem.vue";
import QueueActions from "./Queue/QueueActions.vue";

const queue = useQStore();
const mouseover = ref(false);

function playFromQueue(index: number) {
  queue.play(index);
}

onUpdated(() => {
  if (mouseover.value) return;

  setTimeout(() => {
    focusElem("currentInQueue");
  }, 1000);
});
</script>

<style lang="scss">
.scrollable-r {
  height: 100%;
  overflow: auto;

  .inner {
    // scrollbar-color: grey transparent;
    margin-bottom: 1rem;
  }
}
</style>
