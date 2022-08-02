<template>
  <div class="up-next">
    <div class="r-grid">
      <UpNext :next="queue.tracks[queue.next]" :playNext="queue.playNext" />
      <div class="queue-actions rounded bg-black">
        <div class="left">
          <button class="clear-queue action">Clear</button>
          <button class="shuffle-queue action">Shuffle</button>
          <button class="shuffle-queue action">Shuffle</button>
          <button class="shuffle-queue action">Go to Mix</button>
        </div>
        <div class="right">
          <button class="shuffle-queue action">Save as Playlist</button>
        </div>
      </div>
      <div class="scrollable-r bg-black rounded">
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
    grid-template-rows: max-content max-content 1fr max-content;
    gap: $small;

    .queue-actions {
      display: flex;
      justify-content: space-between;
      gap: $small;
      padding: $small;

      .action {
        background-color: $accent;
        padding: $smaller;
        border-radius: $smaller;
        font-size: 0.8rem;
        padding: inherit 1rem;
      }
    }

    .scrollable-r {
      height: 100%;
      padding: $small 0 $small $small;
      overflow: hidden;

      .inner {
        height: 100%;
        overflow: scroll;
        margin-top: 1rem;
        padding-right: $small;
        overflow-x: hidden;
        scrollbar-color: grey transparent;
      }
    }
  }
}
</style>
