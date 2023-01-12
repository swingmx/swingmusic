<!-- Track component used in app body -->

<template>
  <div
    class="songlist-item rounded-sm"
    :class="[{ current: isCurrent() }, { contexton: context_menu_showing }]"
    @dblclick.prevent="emitUpdate"
    @contextmenu.prevent="showMenu"
  >
    <div
      class="index t-center ellip"
      @click.prevent="addToFav(track.trackhash)"
      @dblclick.prevent.stop="() => {}"
    >
      <div class="text">
        {{ index }}
      </div>
      <div class="heart-icon">
        <HeartFillSvg v-if="is_fav" />
        <HeartSvg v-else />
      </div>
    </div>
    <div class="flex">
      <div @click.prevent="emitUpdate" class="thumbnail">
        <img :src="imguri + track.image" class="album-art image rounded-sm" />
        <div
          class="now-playing-track-indicator image"
          v-if="isCurrent()"
          :class="{ last_played: !isCurrentPlaying() }"
        ></div>
      </div>
      <div v-tooltip class="song-title">
        <div class="with-flag" @click.prevent="emitUpdate">
          <span class="title ellip">
            {{ track.title }}
          </span>
          <MasterFlag v-if="track.bitrate > 1024" />
        </div>
        <div class="isSmallArtists" style="display: none">
          <ArtistName
            :artists="track.artist"
            :albumartists="track.albumartist"
          />
        </div>
      </div>
    </div>
    <div class="song-artists">
      <ArtistName :artists="track.artist" :albumartists="track.albumartist" />
    </div>
    <router-link
      v-if="!hide_album"
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
      @click.stop="showMenu"
      @dblclick.stop="() => {}"
    >
      <OptionSvg />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";

import { showTrackContextMenu as showContext } from "@/composables/context";
import { paths } from "@/config";
import { Track } from "@/interfaces";
import { formatSeconds } from "@/utils";

import HeartSvg from "@/assets/icons/heart.svg";
import HeartFillSvg from "@/assets/icons/heart.fill.svg";
import OptionSvg from "@/assets/icons/more.svg";
import ArtistName from "./ArtistName.vue";

import useQueueStore from "@/stores/queue";
import { favType } from "@/composables/enums";

import MasterFlag from "./MasterFlag.vue";
import favoriteHandler from "@/composables/favoriteHandler";

const imguri = paths.images.thumb.small;
const context_menu_showing = ref(false);
const queue = useQueueStore();

const props = defineProps<{
  track: Track;
  index: Number | String;
  hide_album?: Boolean;
}>();

const is_fav = ref(props.track.is_favorite);

const emit = defineEmits<{
  (e: "playThis"): void;
}>();

function emitUpdate() {
  emit("playThis");
}

function showMenu(e: MouseEvent) {
  showContext(e, props.track, context_menu_showing);
}

function isCurrent() {
  return queue.currenttrackhash == props.track.trackhash;
}

function isCurrentPlaying() {
  return isCurrent() && queue.playing;
}

function addToFav(trackhash: string) {
  favoriteHandler(
    is_fav.value,
    favType.track,
    trackhash,
    () => (is_fav.value = true),
    () => (is_fav.value = false)
  );
}

watch(
  () => props.track.is_favorite,
  (newValue) => {
    is_fav.value = newValue;
  }
);
</script>

<style lang="scss">
.songlist-item {
  display: grid;
  grid-template-columns: 1.75rem 2fr 1fr 1.5fr 2.5rem 2.5rem;
  align-items: center;
  justify-content: flex-start;
  height: $song-item-height;
  gap: 1rem;
  user-select: none;
  padding-left: $small;

  .song-title {
    .with-flag {
      display: flex;
      align-items: center;
    }

    cursor: pointer;

    .title {
      margin-bottom: 2px;
    }
  }

  &:hover {
    background-color: $gray5;

    .index {
      .text {
        transition-delay: 500ms;

        transform: translateX($smaller);
        opacity: 0;
      }

      .heart-icon {
        transition-delay: 500ms;

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
    font-size: 0.8rem;
    width: 100%;
    position: relative;
    height: 3rem;
    display: flex;
    justify-content: center;

    .text {
      opacity: 0.5;
      display: block;
      margin: auto 0;
      transition: all 0.25s;
      width: 100%;
    }

    .heart-icon {
      position: absolute;
      left: -2px;
      display: grid;
      height: 100%;
      align-content: center;
      transition: all 0.2s;
      transform: translateX(-1.5rem);
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

  .context_menu_showing {
    background-color: $gray4;
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

.songlist-item.current {
  background-color: $gray;
}

.songlist-item.contexton {
  background-color: $gray;
}
</style>
