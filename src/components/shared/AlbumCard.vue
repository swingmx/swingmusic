<template>
  <router-link
    :to="{
      name: 'AlbumView',
      params: { hash: album.hash },
    }"
    class="result-item"
  >
    <img class="rounded" :src="imguri + album.image" alt="" />
    <div>
      <h4 class="title ellip" v-tooltip>{{ album.title }}</h4>
      <div class="artist ellip">{{ album.artist }}</div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { AlbumInfo } from "../../interfaces";
import { paths } from "../../config";

const imguri = paths.images.thumb.large;
defineProps<{
  album: AlbumInfo;
}>();
</script>

<style lang="scss">
.result-item {
  display: grid;
  gap: $small;
  padding: $small;
  transition: all 0.5s ease;
  border-radius: 0.7rem;

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
