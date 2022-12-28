<template>
  <div class="f-artists">
    <h3>{{ title }} <span class="see-all">SEE ALL</span></h3>
    <div class="artist-list">
      <ArtistCard
        v-for="artist in artists.slice(0, maxAbumCards)"
        :key="artist.image"
        :artist="artist"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import ArtistCard from "@/components/shared/ArtistCard.vue";
import { Artist } from "@/interfaces";
import { maxAbumCards } from "@/stores/content-width";

defineProps<{
  artists: Artist[];
  title: string;
}>();
</script>

<style lang="scss">
.f-artists {
  h3 {
    display: flex;
    justify-content: space-between;
    padding-left: $medium;
    align-items: center;
    margin-bottom: $small;

    .see-all {
      font-size: $medium;
    }
  }

  .artist-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
  }
}
</style>
