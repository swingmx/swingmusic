<template>
  <div class="xartist" :class="{ _is_on_sidebar: alt }">
    <img class="artist-image shadow-sm" :src="imguri + artist.image" alt="" />
    <div>
      <p class="artist-name t-center ellipsis">{{ artist.name }}</p>
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
.xartist {
  flex: 0 0 auto;
  overflow: hidden;
  position: relative;

  min-width: 8.5em;
  height: 11em;
  border-radius: 0.75rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;

  .artist-image {
    width: 8rem;
    height: 8rem;
    border-radius: 60%;
    margin-bottom: $small;
    transition: all 0.5s ease-in-out;
    transition-delay: 0.25s;
    object-fit: cover;
  }

  &:hover {
    .artist-image {
      border-radius: 20%;
    }
  }

  .artist-name {
    margin: 0;
    font-size: 0.9rem;
    font-weight: 510;
    max-width: 7rem;
    text-transform: capitalize;
  }
}

._is_on_sidebar {
  background-color: $gray4 !important;
}
</style>
