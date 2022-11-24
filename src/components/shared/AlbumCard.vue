<template>
  <router-link
    :to="{
      name: 'AlbumView',
      params: { hash: album.albumhash },
    }"
    class="result-item"
  >
    <img class="rounded" :src="imguri + album.image" alt="" />
    <div>
      <h4 class="title ellip" v-tooltip>{{ album.title }}</h4>
      <div class="artist ellip">{{ album.albumartist }}</div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { paths } from "../../config";
import { AlbumInfo } from "../../interfaces";

const imguri = paths.images.thumb.large;
defineProps<{
  album: AlbumInfo;
}>();
</script>

<style lang="scss">
.result-item {
  display: grid;
  gap: $small;
  padding: $medium;
  border-radius: 1rem;
  height: fit-content;

  &:hover {
    background-color: $gray4;
  }

  img {
    width: 100%;
    height: auto;
  }

  h4 {
    margin: 0;
  }

  .title {
    margin-bottom: $smaller;
    font-size: 0.9rem;
    width: fit-content;
  }

  .artist {
    font-size: 0.8rem;
    text-align: left;
    opacity: 0.75;
  }
}
</style>
