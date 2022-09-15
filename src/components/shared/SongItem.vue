<template>
  <div
    class="songlist-item"
    :class="[{ current: isCurrent }, { contexton: context_on }]"
    @dblclick="emitUpdate(track)"
    @contextmenu.prevent="showMenu"
  >
    <div class="index t-center ellip">
      {{ index }}
    </div>
    <div class="flex">
      <div @click="emitUpdate(track)" class="thumbnail">
        <img
          loading="lazy"
          :src="imguri + track.image"
          alt=""
          class="album-art image rounded-sm"
        />
        <div
          class="now-playing-track-indicator image"
          v-if="isCurrent"
          :class="{ last_played: !isPlaying }"
        ></div>
      </div>
      <div v-tooltip="track.title" class="song-title">
        <div class="title ellip" @click="emitUpdate(track)" ref="artisttitle">
          {{ track.title }}
        </div>
        <div class="isSmallArtists" style="display: none">
          <ArtistName
            :artists="track.artist"
            :albumartist="track.albumartist"
          />
        </div>
      </div>
    </div>
    <div class="song-artists">
      <ArtistName :artists="track.artist" :albumartist="track.albumartist" />
    </div>
    <router-link
      class="song-album ellip"
      v-tooltip="track.album"
      :to="{
        name: 'AlbumView',
        params: {
          hash: track.albumhash || 'Unknown',
        },
      }"
    >
      {{ track.album }}
    </router-link>
    <div class="song-duration">
      <div class="text ellip">{{ formatSeconds(track.duration) }}</div>
    </div>
    <div
      class="options-icon circular"
      :class="{ options_button_clicked }"
      @click.stop="showMenu"
      @dblclick.stop="() => {}"
    >
      <OptionSvg />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import OptionSvg from "@/assets/icons/more.svg";

import { showTrackContextMenu as showContext } from "@/composables/context";
import { paths } from "@/config";
import { Track } from "@/interfaces";
import { formatSeconds } from "@/utils";
import ArtistName from "./ArtistName.vue";

const context_on = ref(false);
const imguri = paths.images.thumb;
const options_button_clicked = ref(false);

const artisttitle = ref<HTMLElement | null>(null);

const props = defineProps<{
  track: Track;
  index: number | string;
  isPlaying: Boolean;
  isCurrent: Boolean;
}>();

const emit = defineEmits<{
  (e: "playThis"): void;
}>();

function emitUpdate(track: Track) {
  emit("playThis");
}

function showMenu(e: Event) {
  showContext(e, props.track, options_button_clicked);
}
</script>

<style lang="scss">
.songlist-item {
  display: grid;
  grid-template-columns: 1.5rem 2fr 1fr 1.5fr 2rem 2.5rem;
  align-items: center;
  justify-content: flex-start;
  height: 3.75rem;
  gap: 1rem;
  user-select: none;

  .song-title {
    cursor: pointer;
  }

  &:hover {
    background-color: $gray4;
  }

  .song-album {
    max-width: max-content;
    cursor: pointer !important;

    &:hover {
      text-decoration: underline;
    }
  }

  .song-artists {
    width: fit-content;
    max-width: 100%;
  }

  .index {
    opacity: 0.5;
    font-size: 0.8rem;
    width: 100%;
  }

  .song-duration {
    font-size: small;
    text-align: left;

    .ellip {
      word-break: keep-all !important;
    }
  }

  .options-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    aspect-ratio: 1;
    width: 2rem;

    svg {
      transition: all 0.2s ease-in;
      stroke: $track-btn-svg;

      circle {
        fill: $track-btn-svg;
      }
    }

    &:hover {
      background-color: $gray5;
    }
  }

  .options_button_clicked {
    background-color: $gray5;
    opacity: 1;
  }

  .flex {
    position: relative;
    align-items: center;

    .thumbnail {
      margin-right: $small;
      display: flex;
    }

    .album-art {
      width: 3rem;
      height: 3rem;
      cursor: pointer;
    }

    .now-playing-track-indicator {
      position: absolute;
      left: $small;
      top: $small;
    }
  }

  td {
    height: 4rem;
    padding: $small;
  }

  td:first-child {
    border-radius: $small 0 0 $small;
  }

  td:nth-child(2) {
    border-radius: 0 $small $small 0;
  }
}
</style>
