<template>
  <div class="artists-results">
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
.right-search .artists-results {
  border-radius: 0.5rem;
  padding: $small;
  margin-bottom: $small;
  border: solid 1px $gray;
  background-color: #150d167c;

  .xartist {
    background: linear-gradient(
      to bottom,
      $gray2 20%,
      $gray4 50%,
      $gray 80%
    );
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: .75rem;
  }
}
</style>
