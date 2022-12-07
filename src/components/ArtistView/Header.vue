<template>
  <div
    class="artist-header-ambient rounded"
    style="height: 100%; width: 100%"
    :style="{
      boxShadow: artist.info.colors
        ? `0 .5rem 2rem ${artist.info.colors[0]}`
        : '',
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
        <div class="card-title">ARTIST</div>
        <div class="artist-name">{{ artist.info.name }}</div>
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
      <PlayBtnRect :source="playSources.artist" :store="useArtistPageStore" />
    </div>
    <div class="artist-img no-select">
      <img :src="paths.images.artist.large + artist.info.image" />
    </div>
    <div
      class="gradient"
      :style="{
        backgroundImage: `linear-gradient(to left, transparent 30%,
      ${artist.info.colors[0]} 50%,
      ${artist.info.colors[0]} 100%)`,
      }"
    ></div>
  </div>
</template>

<script setup lang="ts">
import useArtistPageStore from "@/stores/pages/artist";
import PlayBtnRect from "../shared/PlayBtnRect.vue";
import formatSeconds from "@/utils/useFormatSeconds";
import { isLight } from "@/composables/colors/album";
import { paths } from "@/config";
import { playSources } from "@/composables/enums";

const artist = useArtistPageStore();
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
  grid-template-columns: 1fr 1fr;
  position: relative;

  .artist-img {
    height: 18rem;

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
      $gray2 50%,
      $gray2 100%
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

      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .stats {
      font-size: small;
    }
  }

  .artist-info.nocontrast {
    color: $black;
  }
}
</style>
