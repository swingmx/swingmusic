<template>
  <div class="tracks-results" v-if="tracks">
    <div class="heading theme">TRACKS</div>
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
$theme: #0056f5;

.right-search .tracks-results {
  border-radius: 0.5rem;
  padding: $small;
  border: 2px solid $theme;

  .theme {
    background-image: linear-gradient(
      45deg,
      #21216b 20%,
      $theme 50%,
      #16266b 100%
    );
    color: #fff;
  }
}
</style>
