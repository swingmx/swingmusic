<template>
  <div
    class="songlist-item rounded-sm"
    :class="[{ current: isCurrent }, { contexton: context_on }]"
    @dblclick.prevent="emitUpdate"
    @contextmenu.prevent="showMenu"
  >
    <div class="index t-center ellip" @dblclick.prevent.stop="() => {}">
      <span class="text">
        {{ index }}
      </span>
      <HeartSvg />
    </div>
    <div class="flex">
      <div @click.prevent="emitUpdate" class="thumbnail">
        <img :src="imguri + track.image" class="album-art image rounded-sm" />
        <div
          class="now-playing-track-indicator image"
          v-if="isCurrent"
          :class="{ last_played: !isCurrentPlaying }"
        ></div>
      </div>
      <div v-tooltip class="song-title">
        <div class="title ellip" @click.prevent="emitUpdate" ref="artisttitle">
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
      v-if="!no_album"
      class="song-album ellip"
      v-tooltip
      :to="{
        name: 'AlbumView',
        params: {
          hash: track.albumhash || 'Unknown',
        },
      }"
    >
      {{ track.album }}
    </router-link>
    <div class="song-duration">{{ formatSeconds(track.duration) }}</div>
    <div
      class="options-icon circular"
      :class="{ 'btn-active': options_button_clicked }"
      @click.stop="showMenu"
      @dblclick.stop="() => {}"
    >
      <OptionSvg />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import { showTrackContextMenu as showContext } from "@/composables/context";
import { paths } from "@/config";
import { AlbumDisc, Track } from "@/interfaces";
import { formatSeconds } from "@/utils";

import HeartSvg from "@/assets/icons/heart.svg";
import OptionSvg from "@/assets/icons/more.svg";
import ArtistName from "./ArtistName.vue";

const context_on = ref(false);
const imguri = paths.images.thumb.small;
const options_button_clicked = ref(false);

const artisttitle = ref<HTMLElement | null>(null);

const props = defineProps<{
  track: Track;
  index: Number | String;
  isCurrent: Boolean;
  isCurrentPlaying: Boolean;
  no_album?: Boolean;
}>();

const emit = defineEmits<{
  (e: "playThis"): void;
}>();

function emitUpdate() {
  emit("playThis");
}

function showMenu(e: Event) {
  showContext(e, props.track, options_button_clicked);
}
</script>

<style lang="scss">


.songlist-item {
  display: grid;
  grid-template-columns: 1.5rem 2fr 1fr 1.5fr 2.5rem 2.5rem;
  align-items: center;
  justify-content: flex-start;
  height: $song-item-height;
  gap: 1rem;
  user-select: none;
  padding-left: $small;

  .song-title {
    cursor: pointer;
  }

  &:hover {
    background-color: $gray5;

    .index {
      .text {
        transform: translateX($smaller);
        opacity: 0;
      }

      svg {
        transform: translateX(0);
        opacity: 1;
      }
    }
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
    position: relative;
    height: 3rem;

    .text {
      opacity: 1;
      display: block;
      margin: auto 0;
      transition: all 0.25s;
      transform: translateX(0);
    }

    svg {
      position: absolute;
      left: 0;
      transition: all 0.2s;
      top: $medium;
      opacity: 0;
      transform: translateX(-1rem);
      cursor: pointer;
    }
  }

  .song-duration {
    font-size: small;
    text-align: left;
  }

  .options-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    aspect-ratio: 1;
    width: 2rem;

    svg {
      stroke: $white;
    }

    &:hover {
      background-color: $darkestblue;
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
