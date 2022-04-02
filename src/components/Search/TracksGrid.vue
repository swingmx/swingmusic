<template>
  <div class="tracks-results" v-if="tracks">
    <div class="heading">Tracks</div>
    <div class="items">
      <table>
        <tbody>
          <TrackItem
            v-for="track in props.tracks"
            :key="track.trackid"
            :track="track"
            :isPlaying="queue.playing"
            :isCurrent="queue.current.trackid == track.trackid"
          />
        </tbody>
      </table>
      <LoadMore v-if="more" @loadMore="loadMore" />
    </div>
  </div>
</template>

<script setup>
import LoadMore from "./LoadMore.vue";
import TrackItem from "../shared/TrackItem.vue";
import useQStore from "../../stores/queue";

let counter = 0;
const queue = useQStore();
const props = defineProps({
  tracks: {
    type: Object,
    required: true,
  },
  more: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(["loadMore"]);

function loadMore() {
  counter += 5;
  emit("loadMore", counter);
}
</script>

<style lang="scss">
.right-search .tracks-results {
  border-radius: 0.5rem;
  padding: $small;
  border: 1px solid $gray3;
  // background: ;
}
</style>
