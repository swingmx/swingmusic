<template>
  <div class="xartist" :class="{ _is_on_sidebar: alt }">
    <div
      class="artist-image image bg-black-sm"
      :style="{ backgroundImage: `url('${imguri + artist.image}')` }"
    ></div>
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

  min-width: 8.25em;
  height: 11em;
  border-radius: 0.75rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;

  .artist-image {
    width: 8em;
    height: 8em;
    border-radius: 60%;
    margin-bottom: $small;
    background-size: 8rem 8rem;
    background-position: center;
    background-repeat: no-repeat;
    transition: all 0.5s ease-in-out;
    transition-delay: 0.25s;
  }

  &:hover {
    .artist-image {
      background-position: 50% 20%;
      border-radius: 20%;
      background-size: 10rem 10rem;
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
