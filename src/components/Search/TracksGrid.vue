<template>
  <div class="tracks-results border" v-if="tracks">
    <div class="heading">Tracks</div>
    <TransitionGroup class="items" name="list">
      <TrackItem
        v-for="track in tracks"
        :key="track.trackid"
        :track="track"
        :isPlaying="queue.playing"
        :isCurrent="queue.current.trackid == track.trackid"
        :isSearchTrack="true"
        @PlayThis="updateQueue"
      />
    </TransitionGroup>
    <LoadMore v-if="more" @loadMore="loadMore" />
  </div>
</template>

<script setup lang="ts">
import LoadMore from "./LoadMore.vue";
import TrackItem from "../shared/TrackItem.vue";
import useQStore from "../../stores/queue";
import { Track } from "../../interfaces";

let counter = 0;
const queue = useQStore();

const props = defineProps<{
  tracks: Track[];
  more: boolean;
  query: string;
}>();

const emit = defineEmits(["loadMore"]);

function loadMore() {
  counter += 5;
  emit("loadMore", counter);
}

function updateQueue(track: Track) {
  console.log(props.query);
  queue.playFromSearch(props.query, props.tracks);
  queue.play(track);
}
</script>

<style lang="scss">
.right-search .tracks-results {
  border-radius: 0.5rem;
  padding: $small;

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
