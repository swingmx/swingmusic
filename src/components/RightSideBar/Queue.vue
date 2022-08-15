<template>
  <div class="up-next">
    <div class="r-grid">
      <UpNext :track="queue.tracklist[queue.next]" :playNext="queue.playNext" />
      <div class="scrollable-r bg-black rounded">
        <QueueActions />
        <div
          class="inner"
          @mouseenter="setMouseOver(true)"
          @mouseleave="setMouseOver(false)"
        >
          <TransitionGroup name="queuelist">
            <TrackItem
              v-for="(t, index) in queue.tracklist"
              :key="index"
              :track="t"
              @playThis="queue.play(index)"
              :isCurrent="index === queue.current"
              :isPlaying="queue.playing"
              :isQueueTrack="true"
              :index="index"
            />
          </TransitionGroup>
        </div>
      </div>
      <PlayingFrom :from="queue.from" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onUpdated, ref } from "vue";

import useQStore from "@/stores/queue";
import { focusElem } from "@/utils";

import TrackItem from "../shared/TrackItem.vue";
import PlayingFrom from "./Queue/playingFrom.vue";
import QueueActions from "./Queue/QueueActions.vue";
import UpNext from "./Queue/upNext.vue";

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
.queuelist-move, /* apply transition to moving elements */
.queuelist-enter-active {
  transition: all 0.5s ease-in-out;
}

.queuelist-enter-from,
.queuelist-leave-to {
  opacity: 0;
}

/* ensure leaving items are taken out of layout flow so that moving
   animations can be calculated correctly. */
.queuelist-leave-active {
  transition: none;
  position: absolute;
}

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
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: max-content 1fr max-content;
    gap: $small;

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
