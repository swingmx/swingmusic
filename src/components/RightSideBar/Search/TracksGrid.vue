<template>
  <div id="tracks-results" class="noscroll">
    <div v-if="search.tracks.value.length">
      <TrackComponent
        v-for="(track, index) in search.tracks.value"
        :key="track.trackid"
        :isCurrent="queue.currentid == track.trackid"
        :isHighlighted="false"
        :isPlaying="queue.playing"
        :track="track"
        @playThis="updateQueue(index)"
        :index="index + 1"
      />
    </div>
    <div v-else class="t-center"><h5>💔 No results 💔</h5></div>
    <LoadMore v-if="search.tracks.more" :loader="search.loadTracks" />
  </div>
</template>

<script setup lang="ts">
  import { computed } from "vue";
  
import LoadMore from "./LoadMore.vue";
import TrackItem from "@/components/shared/TrackItem.vue";
import SongItem from "@/components/shared/SongItem.vue";
import useQStore from "@/stores/queue";
import useSearchStore from "@/stores/search";

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
