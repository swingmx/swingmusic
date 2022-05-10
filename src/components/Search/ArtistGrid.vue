<template>
  <div class="artists-results border">
    <div class="heading">Artists</div>
    <div class="grid">
      <ArtistCard v-for="artist in artists" :key="artist" :artist="artist" />
    </div>
    <LoadMore v-if="more" @loadMore="loadMore" />
  </div>
</template>

<script>
import ArtistCard from "@/components/shared/ArtistCard.vue";
import LoadMore from "./LoadMore.vue";

export default {
  props: ["artists", "more"],
  components: {
    ArtistCard,
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
.right-search .artists-results {
  border-radius: 0.5rem;
  padding: $small;
  margin-bottom: $small;

  .xartist {
    background-color: $gray;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
  }
}
</style>
