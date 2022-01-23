<template>
  <div class="tracks-results border" v-if="tracks">
    <div class="heading">🎵 TRACKS</div>
    <div class="items">
      <table>
        <tbody>
          <SongItem v-for="track in tracks" :key="track" :song="track" />
        </tbody>
      </table>
      <LoadMore v-if="more" @loadMore="loadMore" />
    </div>
  </div>
</template>

<script>
import SongItem from "@/components/shared/SongItem.vue";
import LoadMore from "./LoadMore.vue";

export default {
  props: ["tracks", "more"],
  components: {
    SongItem,
    LoadMore,
  },
  setup(props, { emit }) {
    function loadMore() {
      emit("loadMore", "tracks");
    }

    return {
      loadMore,
    };
  },
};
</script>

<style lang="scss">
.right-search .tracks-results {
  border-radius: 0.5rem;
  margin-left: $small;
  padding: $small;
}
</style>