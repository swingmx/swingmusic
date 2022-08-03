<template>
  <router-link
    :to="{
      name: 'AlbumView',
      params: { hash: album.hash },
    }"
    class="result-item"
  >
    <div class="img">
      <div
        class="album-art image"
        :style="{
          backgroundImage: `url(&quot;${imguri + album.image}&quot;)`,
        }"
      ></div>
      <div class="play shadow-lg image"></div>
    </div>
    <div class="title ellip">{{ album.title }}</div>
    <div class="artistsx ellipsis">{{ album.artist }}</div>
  </router-link>
</template>

<script setup lang="ts">
import { AlbumInfo } from "../../interfaces";
import { paths } from "../../config";

const imguri = paths.images.thumb;
defineProps<{
  album: AlbumInfo;
}>();
</script>

<style lang="scss">
.result-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: $small;
  border-radius: 0.75rem;
  text-align: left !important;
  background-color: $gray4;
  color: #ffffffde !important;
  transition: all 0.5s ease;
  min-width: 8.5rem;

  .img {
    position: relative;

    &:hover {
      .play {
        visibility: visible;
      }
    }

    .play {
      width: 3rem;
      height: 3rem;
      background-color: $gray;
      border-radius: 1rem;
      position: absolute;
      left: 2rem;
      bottom: 2.5rem;
      background-image: url("../../assets/icons/play.svg");
      background-size: 2rem;
      background-position: 60% 50%;
      visibility: hidden;
    }

    .album-art {
      height: 7.5rem;
      width: 7.5rem;
      border-radius: 0.5rem;
      margin-bottom: 0.5rem;
    }
  }

  .title {
    width: 7rem;
    margin-bottom: 0.25rem;
    font-size: 0.9rem;
    font-weight: bold;
  }

  .artistsx {
    width: 7rem;
    font-size: 0.8rem;
    text-align: left;
    color: #ffffffbd;
  }
}
</style>
