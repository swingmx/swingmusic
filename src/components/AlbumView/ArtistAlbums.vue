<template>
  <div class="artist-albums">
    <h3>
      <span>{{ title }} </span>
      <span
        class="see-more"
        v-if="maxAbumCards <= albums.length"
        @click="store.setPage(albumType)"
      >
        <RouterLink
          :to="{
            name: Routes.artistDiscography,
            params: { hash: artisthash },
          }"
          >SEE ALL</RouterLink
        >
      </span>
    </h3>
    <div class="cards">
      <AlbumCard v-for="a in albums.slice(0, maxAbumCards)" :album="a" />
    </div>
  </div>
</template>

<script setup lang="ts">
import AlbumCard from "../shared/AlbumCard.vue";
import { Album } from "@/interfaces";

import { maxAbumCards } from "@/stores/content-width";
import { Routes } from "@/router/routes";

import { discographyAlbumTypes } from "@/composables/enums";
import useArtistDiscographyStore from "@/stores/pages/artistDiscog";

const store = useArtistDiscographyStore();

defineProps<{
  title: string;
  artisthash: string;
  albums: Album[];
  albumType: discographyAlbumTypes;
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

    .see-more {
      font-size: $medium;

      a:hover {
        text-decoration: underline;
        cursor: pointer !important;
      }
    }
  }

  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
    gap: 5rem 0;
  }

  .album-card {
    &:hover {
      background-color: $gray;
    }
  }
}
</style>
