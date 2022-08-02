<template>
  <div class="up-next">
    <div class="r-grid">
      <UpNext :next="queue.tracks[queue.next]" :playNext="queue.playNext" />
      <div class="scrollable-r bg-black rounded">
        <div class="queue-actions">
          <div class="left">
            <button class="clear-queue action">
              <ClearSvg />
              <span>Clear</span>
            </button>
            <button class="shuffle-queue action">
              <SaveAsPlaylistSvg />
              <span> Save As Playlist </span>
            </button>
          </div>
          <div class="right">
            <button class="more-action action">
              <MoreSvg />
            </button>
          </div>
        </div>
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
import ClearSvg from "../../assets/icons/delete.svg";
import ShuffleSvg from "../../assets/icons/shuffle.svg";
import SaveAsPlaylistSvg from "../../assets/icons/sdcard.svg";
import MoreSvg from "../../assets/icons/more.svg";

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

    .queue-actions {
      display: flex;
      justify-content: space-between;
      gap: $small;
      margin-bottom: -1.25rem;
      margin-top: $small;

      .action {
        padding: $smaller;
        padding-right: $small;
        background-image: linear-gradient(70deg, $gray3, $gray2);

        svg {
          transform: scale(0.8);
        }
      }

      .more-action {
        padding-right: $smaller;
        svg {
          transform: scale(1.25);
        }
      }
    }

    .scrollable-r {
      height: 100%;
      padding: $small;
      overflow: hidden;
      display: grid;
      grid-template-rows: max-content 1fr;
      gap: $medium;

      .inner {
        height: 100%;
        margin-right: -$small;
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
