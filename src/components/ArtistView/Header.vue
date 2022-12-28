<template>
  <div
    class="artist-header-ambient rounded"
    style="height: 100%; width: 100%"
    :style="{
      boxShadow: artist.info.colors.length
        ? `0 .5rem 2rem ${artist.info.colors[0]}`
        : undefined,
    }"
  ></div>
  <div class="artist-page-header rounded no-scroll">
    <div
      class="artist-info"
      :class="{
        nocontrast: artist.info.colors ? isLight(artist.info.colors[0]) : false,
      }"
    >
      <section class="text">
        <div class="card-title">Artist</div>
        <div class="artist-name ellip2">{{ artist.info.name }}</div>
        <div class="stats">
          {{ artist.info.trackcount }} Track{{
            `${artist.info.trackcount == 1 ? "" : "s"}`
          }}
          • {{ artist.info.albumcount }} Album{{
            `${artist.info.albumcount == 1 ? "" : "s"}`
          }}
          •
          {{ formatSeconds(artist.info.duration, true) }}
        </div>
      </section>
      <div class="buttons">
        <PlayBtnRect :source="playSources.artist" :store="useArtistPageStore" />
        <HeartSvg @handleFav="handleFav" :state="artist.info.is_favorite" />
      </div>
    </div>
    <div class="artist-img no-select">
      <img :src="paths.images.artist.large + artist.info.image" />
    </div>
    <div
      class="gradient"
      :style="{
        backgroundImage: artist.info.colors[0]
          ? `linear-gradient(to left, transparent 30%,
      ${artist.info.colors[0]} 50%,
      ${artist.info.colors[0]} 100%)`
          : '',
      }"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { paths } from "@/config";
import useArtistPageStore from "@/stores/pages/artist";
import formatSeconds from "@/utils/useFormatSeconds";
import { isLight } from "@/composables/colors/album";
import { favType, playSources } from "@/composables/enums";
import favoriteHandler from "@/composables/favoriteHandler";

import PlayBtnRect from "../shared/PlayBtnRect.vue";
import HeartSvg from "@/components/shared/HeartSvg.vue";

const artist = useArtistPageStore();

function handleFav() {
  favoriteHandler(
    artist.info.is_favorite,
    favType.artist,
    artist.info.artisthash,
    artist.makeFavorite,
    artist.removeFavorite
  );
}
</script>

<style lang="scss">
.artist-header-ambient {
  height: 17rem;
  position: absolute;
  opacity: 0.25;
  margin-right: -1rem;
}
.artist-page-header {
  height: 18rem;
  display: grid;
  grid-template-columns: 50% 50%;
  position: relative;

  .artist-img {
    // border: solid red;
    height: 18rem;
    width: 100%;

    img {
      height: 100%;
      width: 100%;
      aspect-ratio: 1;
      object-fit: cover;
      object-position: 0% 20%;
    }
  }

  .gradient {
    position: absolute;
    background-image: linear-gradient(
      to left,
      transparent 10%,
      $gray 50%,
      $gray 100%
    );
    height: 100%;
    width: 100%;
  }

  .artist-info {
    z-index: 1;
    padding: 1rem;
    padding-right: 0;

    display: flex;
    flex-direction: column;
    justify-content: flex-end;

    gap: 1rem;

    .text {
      display: flex;
      flex-direction: column;
      gap: $small;
    }

    .card-title {
      opacity: 0.5;
      font-size: small;
    }

    .artist-name {
      font-size: 3rem;
      font-weight: bold;
      word-wrap: break-word;
    }

    .stats {
      font-size: small;
    }
  }

  .artist-info.nocontrast {
    color: $black;
  }

  .buttons {
    display: flex;
    gap: $small;
  }
}
</style>
