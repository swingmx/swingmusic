<template>
  <div class="up-next">
    <div class="r-grid">
      <PlayingFrom :from="queue.from" />
      <UpNext :next="queue.next" :playNext="queue.playNext" />
      <div class="scrollable-r border rounded">
        <TrackItem
          v-for="t in queue.tracks"
          :key="t.trackid"
          :track="t"
          @playThis="playThis"
          :isCurrent="t.trackid === queue.current.trackid"
          :isPlaying="queue.playing"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import TrackItem from "../shared/TrackItem.vue";
import useQStore from "../../stores/queue";
import { Track } from "../../interfaces.js";
import PlayingFrom from "./queue/playingFrom.vue";
import UpNext from "./queue/upNext.vue";

const queue = useQStore();

function playThis(track: Track) {
  queue.play(track);
}
</script>

<style lang="scss">
.up-next {
  padding: $small $small $small 0;
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
    grid-template-rows: max-content max-content 1fr;

    .scrollable-r {
      height: 100%;
      padding: $small;
      overflow: auto;
      // background-color: $card-dark;
      scrollbar-color: grey transparent;
    }
  }
}
</style>
