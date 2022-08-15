<template>
  <div
    class="songlist-item"
    :class="[
      { current: isCurrent },
      { contexton: context_on },
      {
        highlighted: isHighlighted,
      },
    ]"
    v-bind:class="`track-${track.hash}`"
    @dblclick="emitUpdate(track)"
    @contextmenu.prevent="showMenu"
  >
    <div class="index t-center ellip">{{ index }}</div>
    <div class="flex">
      <div @click="emitUpdate(track)" class="thumbnail">
        <img
          loading="lazy"
          :src="imguri + track.image"
          alt=""
          class="album-art image rounded"
        />
        <div
          class="now-playing-track-indicator image"
          v-if="isCurrent"
          :class="{ last_played: !isPlaying }"
        ></div>
      </div>
      <div @click="emitUpdate(track)">
        <div class="title ellip">
          {{ track.title }}
        </div>
      </div>
    </div>
    <div class="song-artists">
      <div class="ellip" v-if="track.artists[0] !== ''">
        <span
          class="artist"
          v-for="artist in putCommas(track.artists)"
          :key="artist"
          >{{ artist }}</span
        >
      </div>
      <div class="ellip" v-else>
        <span class="artist">{{ track.albumartist }}</span>
      </div>
    </div>
    <router-link
      class="song-album ellip"
      :to="{
        name: 'AlbumView',
        params: {
          hash: track.albumhash,
        },
      }"
    >
      {{ track.album }}
    </router-link>
    <div class="song-duration">
      <div class="text ellip">{{ formatSeconds(track.length) }}</div>
    </div>
    <div
      class="options-icon circular"
      :class="{ options_button_clicked }"
      @click.stop="showMenu"
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
import { formatSeconds, putCommas } from "@/utils";

const context_on = ref(false);
const imguri = paths.images.thumb;
const options_button_clicked = ref(false);

const props = defineProps<{
  track: Track;
  index?: number;
  isPlaying: Boolean;
  isCurrent: Boolean;
  isHighlighted: Boolean;
}>();

const emit = defineEmits<{
  (e: "updateQueue", song: Track): void;
}>();

function emitUpdate(track: Track) {
  emit("updateQueue", track);
}

function showMenu(e: Event) {
  showContext(e, props.track, options_button_clicked);
}
</script>

<style lang="scss">
.songlist-item {
  display: grid;
  grid-template-columns: 1.5rem 1.5fr 1fr 1.5fr 2rem 2.5rem;
  align-items: center;
  justify-items: flex-start;
  height: 3.75rem;
  gap: 1rem;
  user-select: none;

  @include for-desktop-down {
    grid-template-columns: 1.5rem 1.5fr 1fr 2.5rem;

    .song-album {
      display: none !important;
    }

    .song-duration {
      display: none !important;
    }
  }

  @include tablet-portrait {
    grid-template-columns: 1.5rem 1.5fr 1fr 2.5rem;
  }

  &:hover {
    background-color: $gray4;

    .options-icon {
      opacity: 1 !important;
    }
  }

  .song-album {
    word-break: break-all;
    max-width: max-content;
    cursor: pointer;

    &:hover {
      text-decoration: underline;
    }
  }

  .song-artists {
    word-break: break-all;

    .artist {
      cursor: pointer;
    }
  }

  .index {
    opacity: 0.5;
    font-size: 0.8rem;
    width: 100%;
    margin-left: $small;
  }

  .song-duration {
    font-size: 0.9rem;
    text-align: left;
  }

  .options-icon {
    opacity: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    aspect-ratio: 1;
    width: 2rem;

    svg {
      transition: all 0.2s ease-in;
      transform: rotate(90deg);
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

    .title {
      cursor: pointer;
      word-break: break-all;
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

    @include phone-only {
      border-radius: $small;
    }
  }
}
</style>
