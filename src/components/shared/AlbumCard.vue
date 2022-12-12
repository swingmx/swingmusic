<template>
  <RouterLink
    :to="{
      name: 'AlbumView',
      params: { hash: album.albumhash },
    }"
    class="album-card"
  >
    <div class="with-img rounded-sm no-scroll">
      <div
        class="gradient"
        :style="{
          background: `linear-gradient(to top, ${album.colors[0]} 20%, transparent)`,
        }"
      ></div>
      <img class="shadow-lg" :src="imguri + album.image" alt="" />
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
  </RouterLink>
</template>

<script setup lang="ts">
import { paths } from "../../config";
import { Album } from "../../interfaces";
import PlayBtn from "./PlayBtn.vue";

import { playSources } from "@/composables/enums";
import useAlbumStore from "@/stores/pages/album";
import { Routes } from "@/router/routes";

const imguri = paths.images.thumb.large;
defineProps<{
  album: Album;
}>();
</script>

<style lang="scss">
.album-card {
  display: grid;
  gap: $small;
  padding: $medium;
  border-radius: 1rem;

  .with-img {
    position: relative;

    img {
      display: block;
    }

    .gradient {
      position: absolute;
      width: 100%;
      height: 100%;
      opacity: 0;
    }

    &:hover {
      .play-btn {
        transform: translateY(0);
        opacity: 1;
      }

      img {
        border-radius: 0 0 $medium $medium;
      }

      .gradient {
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
