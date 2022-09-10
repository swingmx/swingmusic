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
    <div
      class="info"
      :class="{ nocontrast: album.colors ? isLight(album.colors[0]) : false }"
    >
      <div class="art">
        <img
          :src="imguri.artist + album.artistimg"
          alt=""
          class="circular shadow-lg"
          loading="lazy"
        />
      </div>
      <div>
        <div class="top">
          <div class="h">
            <span v-if="album.is_soundtrack">Soundtrack</span>
            <span v-else-if="album.is_compilation">Compilation</span>
            <span v-else-if="album.is_single">Single</span>
            <span v-else>Album</span>
          </div>
          <div class="title ellip" v-tooltip="album.title">
            {{ album.title }}
          </div>
        </div>
        <div class="bottom">
          <div class="stats">
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
    </div>
    <div
      class="rounded shadow-lg image bigimg"
      :style="{ backgroundImage: `url(${imguri.thumb + album.image})` }"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import { paths } from "@/config";
import useNavStore from "@/stores/nav";
import { AlbumInfo } from "../../interfaces";
import useAlbumStore from "@/stores/pages/album";
import { playSources } from "../../composables/enums";
import { useVisibility, formatSeconds } from "@/utils";
import { getButtonColor, isLight } from "../../composables/colors/album";

import PlayBtnRect from "../shared/PlayBtnRect.vue";

defineProps<{
  album: AlbumInfo;
}>();

const emit = defineEmits<{
  (event: "resetBottomPadding"): void;
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
  if (state) {
    emit("resetBottomPadding");
  }

  nav.toggleShowPlay(state);
}

useVisibility(albumheaderthing, handleVisibilityState);
</script>

<style lang="scss">
.a-header {
  display: grid;
  grid-template-columns: 1fr max-content;
  gap: 1rem;
  padding: 1rem;
  height: 100% !important;
  background-color: $black;
  background-image: linear-gradient(37deg, $black 20%, $gray, $black 90%);
  overflow: hidden;

  .bigimg {
    height: 100%;
    width: 16rem;
    overflow: hidden;

    img {
      height: 100%;
      aspect-ratio: 1;

      object-fit: cover;
      object-position: bottom;
    }
  }

  .nocontrast {
    color: $black;
  }

  .info {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;

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
        // cursor: text;
      }

      .artist {
        font-size: 1.15rem;
      }
    }

    .separator {
      width: 20rem;
    }

    .bottom {
      margin-top: $smaller;

      .stats {
        font-weight: bold;
        font-size: 0.8rem;
        margin-bottom: 0.75rem;

        div {
          width: fit-content;
        }
      }
    }
  }

  @include for-desktop-down {
    .art > img {
      height: 6rem;
      box-shadow: 0 0 1rem $black;
    }

    .info > .top > .title {
      font-size: 2rem;
    }
  }
}
</style>
