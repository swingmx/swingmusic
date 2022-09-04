<template>
  <div class="artist-card" :class="{ _is_on_sidebar: alt }">
    <img
      class="artist-image shadow-sm"
      :src="imguri + artist.image"
      loading="lazy"
    />
    <div>
      <p class="artist-name t-center">{{ artist.name }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Artist } from "@/interfaces";
import { paths } from "../../config";

const imguri = paths.images.artist;

defineProps<{
  artist: Artist;
  alt?: boolean;
}>();
</script>

<style lang="scss">
.artist-card {
  flex: 0 0 auto;
  overflow: hidden;
  position: relative;

  border-radius: 0.75rem;
  display: grid;
  justify-content: center;
  cursor: pointer;

  .artist-image {
    width: 100%;
    border-radius: 60%;
    margin-bottom: $small;
    transition: all 0.5s ease-in-out;
    object-fit: cover;
  }
}
</style>
