<template>
  <div class="albums-results border">
    <div class="heading">💿 ALBUMS</div>
    <div class="grid">
      <AlbumCard v-for="album in albums" :key="album" :album="album" />
    </div>
    <LoadMore v-if="more" @loadMore="loadMore" />
  </div>
</template>

<script>
import AlbumCard from "@/components/shared/AlbumCard.vue";
import LoadMore from "./LoadMore.vue";

export default {
  props: ["albums", "more"],
  components: {
    AlbumCard,
    LoadMore,
  },
  setup(props, { emit }) {
    function loadMore() {
      emit("loadMore");
    }

    return {
      loadMore,
    };
  },
};
</script>

<style lang="scss">
.right-search .albums-results {
  border-radius: 0.5rem;
  background: #0f131b44;

  margin-left: $small;
  margin-top: $small;
  padding:  $small 0;

  .grid {
    display: flex;
    flex-wrap: wrap;
    padding: 0 0 0 $small;
    gap: $small;
  }
}
</style>