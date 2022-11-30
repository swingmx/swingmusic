<template>
  <div class="sidebar-songcard">
    <router-link
      :to="{
        name: 'AlbumView',
        params: {
          hash: track?.albumhash ? track.albumhash : ' ',
        },
      }"
    >
      <img
        :src="imguri + track?.image"
        alt=""
        class="l-image rounded force-lm"
      />
    </router-link>
    <div id="bitrate" v-if="track?.bitrate" title="file type • bitrate">
      {{ track.filetype }} • {{ track.bitrate }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import { paths } from "@/config";
import { Track } from "@/interfaces";

defineProps<{
  track: Track | undefined;
}>();

const imguri = paths.images.thumb.large;
</script>

<style lang="scss">
.sidebar-songcard {
  width: 100%;
  position: relative;
  
  img {
    cursor: pointer;
    width: 100%;
    height: auto;
    aspect-ratio: 1;
    object-fit: cover;
  }

  #bitrate {
    position: absolute;
    font-size: 0.75rem;
    width: max-content;
    padding: 0.2rem 0.35rem;
    bottom: $medium;
    left: $small;
    background-color: $gray4;
    border-radius: $smaller;
    text-transform: uppercase;
  }
}
</style>
