<template>
  <div id="tracks-results" v-if="search.tracks.value">
    <TransitionGroup name="list">
      <TrackItem
        v-for="track in search.tracks.value"
        :key="track.trackid"
        :track="track"
        :isPlaying="queue.playing"
        :isCurrent="queue.current.trackid == track.trackid"
        :isSearchTrack="true"
        @PlayThis="updateQueue"
      />
    </TransitionGroup>
    <LoadMore v-if="search.tracks.more" @loadMore="loadMore" />
  </div>
</template>

<script setup lang="ts">
import LoadMore from "./LoadMore.vue";
import TrackItem from "../../shared/TrackItem.vue";
import useQStore from "../../../stores/queue";
import { Track } from "../../../interfaces";
import useSearchStore from "../../../stores/search";

const queue = useQStore();
const search = useSearchStore();

function loadMore() {
    search.updateLoadCounter("tracks", 5);
  search.loadTracks(search.loadCounter.tracks);
}

function updateQueue(track: Track) {
  queue.playFromSearch(search.query, search.tracks.value);
  queue.play(track);
}
</script>

<style lang="scss">
.right-search #tracks-results {
  border-radius: 0.5rem;
  padding: $small;
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
