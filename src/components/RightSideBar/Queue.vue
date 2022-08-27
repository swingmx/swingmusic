<template>
  <div class="up-next">
    <div class="r-grid">
      <div class="scrollable-r rounded">
        <QueueActions />
        <div
          class="inner"
          @mouseenter="setMouseOver(true)"
          @mouseleave="setMouseOver(false)"
        >
          <TrackItem
            v-for="(t, index) in queue.tracklist"
            :key="index"
            :track="t"
            @playThis="queue.play(index)"
            :isCurrent="index === queue.currentindex"
            :isPlaying="queue.playing"
            :isQueueTrack="true"
            :index="index"
          />
        </div>
      </div>
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

function setMouseOver(val: boolean) {
  mouseover.value = val;
}

onUpdated(() => {
  if (mouseover.value) return;

  setTimeout(() => {
    focusElem("currentInQueue");
  }, 1000);
});
</script>

<style lang="scss">
.up-next {
  overflow: hidden;
  height: 100%;

  .heading {
    position: relative;
    margin: 0.5rem 0 1rem 0;
  }

  .r-grid {
    position: relative;
    height: 100%;

    .scrollable-r {
      height: 100%;
      overflow: hidden;
      display: grid;
      grid-template-rows: max-content 1fr;

      .inner {
        overflow: scroll;
        overflow-x: hidden;
        scrollbar-color: grey transparent;
        margin: 1rem 0;
      }
    }
  }
}
</style>
