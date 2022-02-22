<template>
  <div class="artists-results">
    <div class="heading theme">ARTISTS</div>
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
$theme: #464545fd;

.right-search .artists-results {
  border-radius: 0.5rem;
  background: #1214178c;
  padding: $small;
  margin-bottom: $small;
  border: solid 2px $theme;

  .xartist:hover {
    border: solid 2px $theme;
  }

  .theme {
    background-image: linear-gradient(
      45deg,
      #141414 0%,
      #464545fd 50%,
      #111111 100%
    );
    color: #fff;
  }

  .grid {
    display: flex;
    flex-wrap: wrap;
  }
}
</style>
