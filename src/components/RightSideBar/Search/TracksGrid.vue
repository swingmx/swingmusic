<template>
  <div id="tracks-results" class="no-scroll">
    <div v-if="search.tracks.value.length">
      <TrackComponent
        v-for="(track, index) in search.tracks.value"
        :key="track.id"
        :isCurrent="queue.currenttrackhash === track.trackhash"
        :isHighlighted="false"
        :isCurrentPlaying="
          queue.currenttrackhash === track.trackhash && queue.playing
        "
        :track="track"
        @playThis="updateQueue(index)"
        :index="index + 1"
      />
    </div>
    <div v-else class="t-center"><h5>💔 No results 💔</h5></div>
    <LoadMore
      :loader="search.loadTracks"
      :can_load_more="search.tracks.more"
      v-if="search.tracks.value.length"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";

import SongItem from "@/components/shared/SongItem.vue";
import TrackItem from "@/components/shared/TrackItem.vue";
import useQStore from "@/stores/queue";
import useSearchStore from "@/stores/search";
import LoadMore from "./LoadMore.vue";

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

onMounted(() => {
  search.switchTab("tracks");
});
</script>

<style lang="scss">
#tracks-results .morexx {
  margin-top: 1rem;
}
</style>
