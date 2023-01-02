<template>
  <div class="f-artists">
    <h3>
      {{ title }}
      <SeeAll :route="route" />
    </h3>
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
import SeeAll from "../shared/SeeAll.vue";

defineProps<{
  artists: Artist[];
  title: string;
  route: string;
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

   
  }

  .artist-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(9rem, 1fr));
  }
}
</style>
