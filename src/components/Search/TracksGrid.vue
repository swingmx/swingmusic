<template>
  <div class="tracks-results border" v-if="tracks">
    <div class="heading">🎵 TRACKS</div>
    <div class="items">
      <table>
        <tbody>
          <SongItem
            v-for="(track, index) in props.tracks"
            :key="track"
            :song="track"
            :index="index + 1"
          />
        </tbody>
      </table>
      <LoadMore v-if="more" @loadMore="loadMore" />
    </div>
  </div>
</template>

<script setup>
import SongItem from "@/components/shared/SongItem.vue";
import LoadMore from "./LoadMore.vue";

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
  margin-left: $small;
  padding: $small;
}
</style>
