<template>
  <div id="tracks-results">
    <div v-if="search.tracks.value.length">
      <div>
        <TrackComponent
          v-for="(track, index) in search.tracks.value"
          :key="track.trackid"
          :isCurrent="queue.currentid == track.trackid"
          :isHighlighted="false"
          :isPlaying="queue.playing"
          :track="track"
          @PlayThis="updateQueue(index)"
        />
      </div>
    </div>
    <div v-else class="t-center"><h5>🤷</h5></div>
    <LoadMore v-if="search.tracks.more" :loader="search.loadTracks" />
  </div>
</template>

<script setup lang="ts">
import LoadMore from "./LoadMore.vue";
import TrackItem from "@/components/shared/TrackItem.vue";
import SongItem from "@/components/shared/SongItem.vue";
import useQStore from "../../../stores/queue";
import useSearchStore from "../../../stores/search";
import { computed } from "vue";

const queue = useQStore();
const search = useSearchStore();

function updateQueue(index: number) {
  queue.playFromSearch(search.query, search.tracks.value);
  queue.play(index);
}

const props = defineProps<{
  isOnSearchPage?: boolean;
}>();

const TrackComponent = computed(() => {
  if (props.isOnSearchPage) {
    return SongItem;
  }

  return TrackItem;
});

let use_song_item: boolean = false;

if (props.isOnSearchPage) {
  use_song_item = true;
}
</script>

<style lang="scss">
.right-search #tracks-results {
  height: 100% !important;
  overflow: hidden;
}
</style>
