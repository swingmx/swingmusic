<template>
  <div class="up-next">
    <div class="r-grid">
      <UpNext :next="queue.next" :playNext="queue.playNext" />
      <div
        class="scrollable-r border rounded"
        @mouseenter="setMouseOver(true)"
        @mouseleave="setMouseOver(false)"
      >
        <TrackItem
          v-for="t in queue.tracks"
          :key="t.trackid"
          :track="t"
          @playThis="queue.play(t)"
          :isCurrent="t.trackid === queue.current.trackid"
          :isPlaying="queue.playing"
        />
      </div>
      <PlayingFrom :from="queue.from" />
    </div>
  </div>
</template>

<script setup lang="ts">
import TrackItem from "../shared/TrackItem.vue";
import useQStore from "../../stores/queue";
import PlayingFrom from "./queue/playingFrom.vue";
import UpNext from "./queue/upNext.vue";
import { onUpdated, ref } from "vue";
import { focusElem } from "@/composables/perks";

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

    .scrollable-r {
      height: 100%;
      padding: $small;
      overflow: auto;
      overflow-x: hidden;
      scrollbar-color: grey transparent;
    }
  }
}
</style>
