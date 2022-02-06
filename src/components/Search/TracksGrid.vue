<template>
  <div class="tracks-results border" v-if="tracks">
    <div class="heading">🎵 TRACKS</div>
    <div class="items">
      <table>
        <tbody>
          <TrackItem
            v-for="track in props.tracks"
            :key="track.track_id"
            :track="track"
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

const emit = defineEmits(["loadMore"])

function loadMore() {
  emit("loadMore", "tracks");
}
</script>

<style lang="scss">
.right-search .tracks-results {
  border-radius: 0.5rem;
  padding: $small;
}
</style>
