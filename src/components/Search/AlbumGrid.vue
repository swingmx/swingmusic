<template>
  <div class="albums-results">
    <div class="heading">Albums</div>
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
    let counter = 0;

    function loadMore() {
      counter += 6;
      emit("loadMore", counter);
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
  margin-top: $small;
  padding: $small;
  overflow-x: hidden;
  border: solid 1px $gray;

  .result-item:hover {
    background-color: $gray3;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(8rem, 1fr));
    flex-wrap: wrap;
    gap: 0.75rem;
  }
}
</style>
