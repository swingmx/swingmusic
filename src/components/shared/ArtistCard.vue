<template>
  <div class="artist-card" :class="{ _is_on_sidebar: alt }">
    <img class="artist-image circular" :src="imguri + artist.image" loading="lazy" />
    <div class="artist-name t-center">
      {{ artist.name }}
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

  border-radius: $medium;
  display: grid;
  gap: $small;
  justify-content: center;
  padding: 1.2rem 1rem !important;
  font-size: 0.9rem;
  font-weight: bolder;
  height: fit-content;

  &:hover {
    background-color: $gray4;
  }

  .artist-image {
    width: 100%;
    // margin-bottom: $small;
    transition: all 0.5s ease-in-out;
    object-fit: cover;
  }
}
</style>
