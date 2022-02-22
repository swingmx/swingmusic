<template>
  <div class="artists-results">
    <div class="heading">ARTISTS</div>
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
$theme: #585858cc;

.right-search .artists-results {
  border-radius: 0.5rem;
  background: #1214178c;
  padding: $small;
  margin-bottom: $small;
  border: solid 2px $theme;

  .xartist:hover {
    border: solid 2px $theme;
  }

  .heading {
    background-color: $theme;
    color: #fff;
  }

  .morexx > button {
    background-color: $theme !important;
    color: #fff;
  }

  .grid {
    display: flex;
    flex-wrap: wrap;
  }
}
</style>
