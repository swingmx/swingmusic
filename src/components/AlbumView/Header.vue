<template>
  <div
    class="a-header rounded"
    ref="albumheaderthing"
    :style="{
      backgroundImage: `linear-gradient(
        37deg, ${props.album.colors[0]}, ${props.album.colors[3]}
      )`,
    }"
  >
    <div class="art rounded">
      <img
        :src="imguri + album.image"
        alt=""
        v-motion-slide-from-left
        class="rounded shadow-lg"
      />
    </div>
    <div class="info" :class="{ nocontrast: isLight() }">
      <div class="top" v-motion-slide-from-top>
        <div class="h">
          <span v-if="album.is_soundtrack">Soundtrack</span>
          <span v-else-if="album.is_compilation">Compilation</span>
          <span v-else-if="album.is_single">Single</span>
          <span v-else>Album</span>
        </div>
        <div class="title ellip">
          {{ album.title }}
        </div>
      </div>
      <div class="bottom">
        <div class="stats">
          {{ album.count }} Tracks • {{ formatSeconds(album.duration, true) }} •
          {{ album.date }} •
          {{ album.artist }}
        </div>
        <PlayBtnRect
          :source="playSources.album"
          :store="useAlbumStore"
          :background="getButtonColor()"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import useVisibility from "@/composables/useVisibility";
import useNavStore from "@/stores/nav";
import useAlbumStore from "@/stores/pages/album";
import { ref } from "vue";
import { playSources } from "../../composables/enums";
import { formatSeconds } from "../../composables/perks";
import { paths } from "@/config";
import { AlbumInfo } from "../../interfaces";
import PlayBtnRect from "../shared/PlayBtnRect.vue";

const props = defineProps<{
  album: AlbumInfo;
}>();

const emit = defineEmits<{
  (event: "resetBottomPadding"): void;
}>();

const albumheaderthing = ref<HTMLElement>(null);
const imguri = paths.images.thumb;
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

/**
 * Returns `true` if the rgb color passed is light.
 *
 * @param {string} rgb The color to check whether it's light or dark.
 * @returns {boolean} true if color is light, false if color is dark.
 */
function isLight(rgb: string = props.album.colors[0]): boolean {
  if (rgb == null || undefined) return false;

  const [r, g, b] = rgb.match(/\d+/g)!.map(Number);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;

  return brightness > 170;
}

interface BtnColor {
  color: string;
  isDark: boolean;
}

/**
 * Returns the first contrasting color in the album colors.
 *
 * @param {string[]} colors The album colors to choose from.
 * @returns {BtnColor} A color to use as the play button background
 */
function getButtonColor(colors: string[] = props.album.colors): BtnColor {
  const base_color = colors[0];
  if (colors.length === 0) return { color: "#fff", isDark: true };

  for (let i = 0; i < colors.length; i++) {
    if (theyContrast(base_color, colors[i])) {
      return {
        color: colors[i],
        isDark: isLight(colors[i]),
      };
    }
  }

  return {
    color: "#fff",
    isDark: true,
  };
}

/**
 * Returns the luminance of a color.
 * @param r The red value of the color.
 * @param g The green value of the color.
 * @param b The blue value of the color.
 */
function luminance(r: any, g: any, b: any) {
  let a = [r, g, b].map(function (v) {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
}

/**
 * Returns a contrast ratio of `color1`:`color2`
 * @param {string} color1 The first color
 * @param {string} color2 The second color
 */
function contrast(color1: number[], color2: number[]): number {
  let lum1 = luminance(color1[0], color1[1], color1[2]);
  let lum2 = luminance(color2[0], color2[1], color2[2]);
  let brightest = Math.max(lum1, lum2);
  let darkest = Math.min(lum1, lum2);
  return (brightest + 0.05) / (darkest + 0.05);
}

/**
 * Converts a rgb color string to an array of the form: `[r, g, b]`
 * @param rgb The color to convert
 * @returns {number[]} The array representation of the color
 */
function rgbToArray(rgb: string): number[] {
  return rgb.match(/\d+/g)!.map(Number);
}

/**
 * Returns true if the `color2` contrast with `color1`.
 * @param color1 The first color
 * @param color2 The second color
 */
function theyContrast(color1: string, color2: string) {
  return contrast(rgbToArray(color1), rgbToArray(color2)) > 3;
}
</script>

<style lang="scss">
.a-header {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 1rem;
  padding: 1rem;
  height: 100% !important;
  background-color: $black;
  background-image: linear-gradient(37deg, $black 20%, $gray, $black 90%);

  .art {
    display: flex;
    align-items: flex-end;
    position: relative;
    overflow: hidden;

    img {
      height: 16rem;
      aspect-ratio: 1;
      object-fit: cover;
      transition: all 0.2s ease-in-out;
      user-select: none;
    }
  }

  .nocontrast {
    color: $black;
  }

  .info {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;

    .top {
      .title {
        font-size: 2.5rem;
        font-weight: 600;
        text-transform: capitalize;
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
        border-radius: $small;
        font-weight: bold;
        font-size: 0.8rem;
        margin-bottom: 0.75rem;
      }
    }
  }
}
</style>
