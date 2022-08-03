<template>
  <div class="up-next">
    <div class="r-grid">
      <UpNext :next="queue.tracks[queue.next]" :playNext="queue.playNext" />
      <div class="scrollable-r bg-black rounded">
        <QueueActions />
        <div
          class="inner"
          @mouseenter="setMouseOver(true)"
          @mouseleave="setMouseOver(false)"
        >
          <TrackItem
            v-for="(t, index) in queue.tracks"
            :key="t.trackid"
            :track="t"
            @playThis="queue.play(index)"
            :isCurrent="index === queue.current"
            :isPlaying="queue.playing"
          />
        </div>
      </div>
      <PlayingFrom :from="queue.from" />
    </div>
  </div>
</template>

<script setup lang="ts">
import TrackItem from "../shared/TrackItem.vue";
import useQStore from "@/stores/queue";
import PlayingFrom from "./Queue/playingFrom.vue";
import UpNext from "./Queue/upNext.vue";
import { onUpdated, ref } from "vue";
import { focusElem } from "@/composables/perks";
import QueueActions from "./Queue/QueueActions.vue";

const queue = useQStore();
const mouseover = ref(false);

function setMouseOver(val: boolean) {
  mouseover.value = val;
}

onUpdated(() => {
  if (mouseover.value) return;

  focusElem("currentInQueue");
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
    display: grid;
    grid-template-rows: max-content 1fr max-content;
    gap: $small;

    .left {
      display: flex;
      gap: $small;
    }

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
