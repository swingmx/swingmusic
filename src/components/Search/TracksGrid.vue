<template>
  <div class="tracks-results" v-if="tracks">
    <div class="heading">TRACKS</div>
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

const emit = defineEmits(["loadMore"]);

function loadMore() {
  emit("loadMore", "tracks");
}
</script>

<style lang="scss">
$theme: rgb(86, 86, 87);

.right-search .tracks-results {
  border-radius: 0.5rem;
  padding: $small;
  border: 2px solid $theme;

  .heading {
    background-color: $theme;
    color: #fff;
  }

  .morexx > button {
    background-color: $theme !important;
    color: #fff;
  }
}
</style>
