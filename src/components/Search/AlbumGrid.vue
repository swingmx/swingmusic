<template>
  <div class="albums-results">
    <div class="heading theme">ALBUMS</div>
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
$theme: #6405d1;

.right-search .albums-results {
  border-radius: 0.5rem;
  background: #0f131b44;
  margin-top: $small;
  padding: $small;
  overflow-x: hidden;
  border: solid 2px $theme;

  .result-item:hover {
    border: solid 2px $theme;
  }

  .theme {
    background-image: linear-gradient(
      45deg,
      #380079 20%,
      #6405d1 50%,
      #1b0342 100%
    );
    color: #fff;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(8rem, 1fr));
    flex-wrap: wrap;
    gap: $small;
  }
}
</style>
