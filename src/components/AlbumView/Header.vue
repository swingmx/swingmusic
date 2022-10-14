<template>
  <div
    class="a-header rounded"
    ref="albumheaderthing"
    :style="{
      backgroundImage: album.colors
        ? `linear-gradient(
        37deg, ${album.colors[0]}, ${album.colors[3]}
      )`
        : '',
    }"
  >
    <div class="big-img no-scroll" :class="{ imgSmall: albumHeaderSmall }">
      <img :src="imguri.thumb.large + album.image" class="rounded" />
    </div>
    <div
      class="info"
      :class="{ nocontrast: album.colors ? isLight(album.colors[0]) : false }"
    >
      <div class="album-info">
        <div class="top">
          <div v-auto-animate class="h">
            <span v-if="album.is_soundtrack">Soundtrack</span>
            <span v-else-if="album.is_compilation">Compilation</span>
            <span v-else-if="album.is_single">Single</span>
            <span v-else>Album</span>
          </div>
          <div class="title ellip" v-tooltip>
            {{ album.title }}
          </div>
        </div>
        <div class="bottom">
          <div class="stats ellip">
            <div class="border rounded-sm pad-sm">
              {{ album.artist }} • {{ album.date }} • {{ album.count }}
              {{ album.count === 1 ? "Track" : "Tracks" }} •
              {{ formatSeconds(album.duration, true) }}
            </div>
          </div>
          <PlayBtnRect
            :source="playSources.album"
            :store="useAlbumStore"
            :background="getButtonColor(album.colors)"
          />
        </div>
      </div>
      <div class="art" v-if="!albumHeaderSmall">
        <img
          :src="imguri.artist + album.artistimg"
          class="shadow-lg circular"
          loading="lazy"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import { paths } from "@/config";
import { albumHeaderSmall } from "@/stores/content-width";
import useNavStore from "@/stores/nav";
import useAlbumStore from "@/stores/pages/album";
import { formatSeconds, useVisibility } from "@/utils";
import { getButtonColor, isLight } from "../../composables/colors/album";
import { playSources } from "../../composables/enums";
import { AlbumInfo } from "../../interfaces";

import PlayBtnRect from "../shared/PlayBtnRect.vue";

defineProps<{
  album: AlbumInfo;
}>();

const albumheaderthing = ref<any>(null);
const imguri = paths.images;
const nav = useNavStore();

/**
 * Calls the `toggleShowPlay` method which toggles the play button in the nav.
 * Emits the `resetBottomPadding` event to reset the album page content bottom padding.
 *
 * @param {boolean} state the new visibility state of the album page header.
 */
function handleVisibilityState(state: boolean) {
  nav.toggleShowPlay(state);
}

useVisibility(albumheaderthing, handleVisibilityState);
</script>

<style lang="scss">
.a-header {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 1rem;
  padding: 1rem;
  height: $banner-height;
  background-color: $black;
  overflow: hidden;

  .big-img {
    height: calc(100%);
    width: 16rem;
    display: flex;
    align-items: flex-end;

    img {
      height: 16rem;
      aspect-ratio: 1;
    }
  }

  .big-img.imgSmall {
    width: 12rem;

    img {
      height: 12rem;
    }
  }

  .nocontrast {
    color: $black;
  }

  .info {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr max-content;
    height: 100%;
    align-items: flex-end;

    .art {
      display: flex;
      align-items: flex-end;
    }

    img {
      height: 6rem;
      aspect-ratio: 1;
      object-fit: cover;
      user-select: none;
    }

    .top {
      .h {
        font-size: 14px;
        opacity: 0.5;
      }

      .title {
        font-size: 2.5rem;
        font-weight: 600;
        width: fit-content;
        cursor: text;
      }

      .artist {
        font-size: 1.15rem;
      }
    }

    .bottom {
      margin-top: $smaller;

      .stats {
        font-weight: bold;
        font-size: 0.8rem;
        margin-bottom: 0.75rem;

        div {
          width: fit-content;
          cursor: text;
        }
      }
    }
  }
}
</style>
