<template>
  <div class="artist-albums">
    <h3>
      <span>{{ title }} </span>
      <SeeAll
        v-if="maxAbumCards <= albums.length"
        :route="route"
        @click="
          !favorites ? useArtistDiscographyStore().setPage(albumType) : null
        "
      />
    </h3>
    <div class="cards">
      <AlbumCard v-for="a in albums.slice(0, maxAbumCards)" :album="a" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Album } from "@/interfaces";
import { maxAbumCards } from "@/stores/content-width";
import { discographyAlbumTypes } from "@/composables/enums";
import useArtistDiscographyStore from "@/stores/pages/artistDiscog";

import AlbumCard from "../shared/AlbumCard.vue";
import SeeAll from "../shared/SeeAll.vue";

defineProps<{
  title: string;
  albums: Album[];
  albumType?: discographyAlbumTypes;
  favorites?: boolean;
  route: string;
}>();
</script>

<style lang="scss">
.artist-albums {
  overflow: hidden;

  h3 {
    display: grid;
    grid-template-columns: 1fr max-content;
    align-items: center;
    padding: 0 $medium;
    margin-bottom: $small;
  }

  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(9rem, 1fr));
    gap: 5rem 0;
  }

  .album-card {
    &:hover {
      background-color: $gray;
    }
  }
}
</style>
