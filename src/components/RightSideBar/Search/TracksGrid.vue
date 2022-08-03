<template>
  <div id="tracks-results" v-if="search.tracks.value">
    <TransitionGroup name="list">
      <TrackItem
        v-for="(track, index) in search.tracks.value"
        :key="track.trackid"
        :track="track"
        :isPlaying="queue.playing"
        :isCurrent="queue.currentid == track.trackid"
        :isSearchTrack="true"
        @PlayThis="updateQueue(index)"
      />
    </TransitionGroup>
    <LoadMore v-if="search.tracks.more" @loadMore="loadMore" />
  </div>
</template>

<script setup lang="ts">
import LoadMore from "./LoadMore.vue";
import TrackItem from "../../shared/TrackItem.vue";
import useQStore from "../../../stores/queue";
import useSearchStore from "../../../stores/search";

const queue = useQStore();
const search = useSearchStore();

function loadMore() {
  search.updateLoadCounter("tracks");
  search.loadTracks(search.loadCounter.tracks);
}

function updateQueue(index: number) {
  queue.playFromSearch(search.query, search.tracks.value);
  queue.play(index);
}
</script>

<style lang="scss">
.right-search #tracks-results {
  height: 100% !important;
  overflow: hidden;

  .list-enter-active,
  .list-leave-active {
    transition: all 0.5s ease;
    transition-delay: 0.5s;
  }
  .list-enter-from,
  .list-leave-to {
    opacity: 0;
    transform: translateY(2rem);
  }
}
</style>
