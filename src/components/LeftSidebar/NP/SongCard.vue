<template>
  <div class="sidebar-songcard">
    <div class="art">
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
      <div id="bitrate" v-if="track?.bitrate">
        {{ track.filetype }}• {{ track.bitrate }}
      </div>
      <div class="heart rounded-sm" @click="heartClicked = !heartClicked">
        <HeartSvg v-if="!heartClicked" />
        <HeartFilledSvg v-else />
      </div>
    </div>

    <div class="bottom">
      <div class="title ellip t-center" v-tooltip>
        {{ track?.title || "♥ Hello ♥" }}
      </div>
      <ArtistName
        :artists="track?.artist || []"
        :albumartist="track?.albumartist || 'Play something'"
        :small="true"
        class="artists"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import { paths } from "@/config";
import { Track } from "@/interfaces";
import ArtistName from "@/components/shared/ArtistName.vue";

import HeartSvg from "@/assets/icons/heart.svg";
import HeartFilledSvg from "@/assets/icons/heart.fill.svg";

defineProps<{
  track: Track | null;
}>();

const heartClicked = ref<boolean>(false);

const imguri = paths.images.thumb.large;
</script>

<style lang="scss">
.sidebar-songcard {
  .art {
    width: 100%;
    aspect-ratio: 1;
    place-items: center;
    margin-bottom: $small;
    position: relative;

    .heart {
      position: absolute;
      bottom: -$smaller;
      right: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      border-radius: $smaller;
    }

    img {
      width: 100%;
      height: auto;
      aspect-ratio: 1;
      object-fit: cover;
      cursor: pointer;
      margin-bottom: 2rem;
    }

    #bitrate {
      position: absolute;
      font-size: 0.75rem;
      width: max-content;
      padding: 0.2rem 0.35rem;
      bottom: $smaller;
      left: 0;
      background-color: $gray4;
      border-radius: $smaller;
      text-transform: uppercase;
    }
  }

  .bottom {
    display: grid;
    gap: $smaller;
  }

  .title {
    font-weight: 900;
    margin: 0 auto;
  }
  
  .artists {
    opacity: 0.5;
    margin: 0 auto;

    &:hover {
      text-decoration: underline 1px !important;
    }
  }
}
</style>
