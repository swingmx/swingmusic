<template>
  <router-link
    :to="{
      name: 'AlbumView',
      params: { hash: album.albumhash },
    }"
    class="result-item"
    :class="{
      nocontrast: album.colors ? isLight(album.colors[0]) : false,
    }"
  >
    <div
      class="bg rounded"
      :style="{
        backgroundColor: `${
          album.colors[0] ? album.colors[0] : 'rgb(72, 72, 74)'
        }`,
      }"
    ></div>
    <div class="with-img">
      <img class="rounded-sm shadow-lg" :src="imguri + album.image" alt="" />
      <PlayBtn
        :store="useAlbumStore"
        :source="playSources.album"
        :albumHash="album.albumhash"
        :albumName="album.title"
      />
    </div>
    <div>
      <h4 class="title ellip" v-tooltip>
        {{ album.title }}
      </h4>
      <div class="artist ellip" @click.prevent.stop="() => {}">
        <RouterLink
          :to="{
            name: Routes.artist,
            params: { hash: album.albumartists[0].artisthash },
          }"
        >
          {{ album.albumartists[0].name }}
        </RouterLink>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { paths } from "../../config";
import { Album } from "../../interfaces";
import { isLight } from "@/composables/colors/album";
import PlayBtn from "./PlayBtn.vue";

import useAlbumStore from "@/stores/pages/album";
import { playSources, Routes } from "@/composables/enums";

const imguri = paths.images.thumb.large;
defineProps<{
  album: Album;
}>();
</script>

<style lang="scss">
.result-item.nocontrast {
  &:hover {
    color: $black;
  }
}

.result-item {
  display: grid;
  gap: $small;
  padding: $medium;
  border-radius: 1rem;
  height: fit-content;
  position: relative;
  color: $white;

  .with-img {
    position: relative;
    padding: 0;

    &:hover {
      .play-btn {
        transform: translateY(0);
        opacity: 1;
      }
    }
  }

  .play-btn {
    $btn-width: 4rem;
    position: absolute;
    bottom: 1rem;
    right: calc((100% - $btn-width) / 2);
    opacity: 0;
    transform: translateY(1rem);
    transition: all 0.25s;
    width: $btn-width;

    &:hover {
      transition: all 0.25s;
      background: $darkestblue;
    }
  }

  .bg {
    height: 100%;
    width: 100%;
    position: absolute;
    opacity: 0;
  }

  &:hover {
    .bg {
      opacity: 1;
    }
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
    position: relative;
  }

  .artist {
    font-size: 0.8rem;
    text-align: left;
    opacity: 0.75;

    a {
      cursor: pointer !important;

      &:hover {
        text-decoration: underline;
      }
    }
  }
}
</style>
