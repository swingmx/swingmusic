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
    v-bind:class="`track-${track.uniq_hash}`"
    @dblclick="emitUpdate(track)"
    @contextmenu="showContextMenu"
  >
    <div class="index t-center">{{ index }}</div>
    <div class="flex">
      <div @click="emitUpdate(track)" class="thumbnail">
        <img
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
        <span class="ellip title cap-first">{{ track.title }}</span>
      </div>
    </div>
    <div class="song-artists cap-first">
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
      class="song-album ellip cap-first"
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
      <div class="text">{{ formatSeconds(track.length) }}</div>
    </div>
    <div
      class="options-icon circular"
      :class="{ options_button_clicked }"
      @click="
        (e) => {
          showContextMenu(e);
          options_button_clicked = true;
        }
      "
    >
      <OptionSvg />
    </div>
  </div>
</template>

<script setup lang="ts">
import OptionSvg from "@/assets/icons/more.svg";
import { ContextSrc } from "@/composables/enums";
import { formatSeconds, putCommas } from "@/composables/perks";
import useContextStore from "@/stores/context";
import useModalStore from "@/stores/modal";
import useQueueStore from "@/stores/queue";

import { paths } from "@/config";
import trackContext from "@/contexts/track_context";
import { Track } from "@/interfaces";
import { ref } from "vue";

const contextStore = useContextStore();

const context_on = ref(false);
const imguri = paths.images.thumb;
const options_button_clicked = ref(false);

const showContextMenu = (e: Event) => {
  e.preventDefault();
  e.stopPropagation();

  const menus = trackContext(props.track, useModalStore, useQueueStore);

  contextStore.showContextMenu(e, menus, ContextSrc.Track);
  context_on.value = true;

  contextStore.$subscribe((mutation, state) => {
    if (!state.visible) {
      context_on.value = false;
      options_button_clicked.value = false;
    }
  });
};

const props = defineProps<{
  track: Track;
  index: Number;
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
</script>

<style lang="scss">
.songlist-item {
  display: grid;
  align-items: center;
  grid-template-columns: 1.5rem 1.5fr 1fr 1.5fr 2rem 2.5rem;
  height: 3.75rem;
  text-align: left;
  gap: $small;
  user-select: none;

  @include tablet-landscape {
    grid-template-columns: 1.5rem 1.5fr 1fr 1fr 2.5rem;
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

  .song-duration {
    @include tablet-landscape {
      display: none !important;
    }
  }

  .song-album {
    word-break: break-all;
    max-width: max-content;
    cursor: pointer;

    &:hover {
      text-decoration: underline;
    }

    @include tablet-portrait {
      display: none;
    }
  }

  .song-artists {
    word-break: break-all;

    .artist {
      cursor: pointer;
    }

    @include phone-only {
      display: none;
    }
  }

  .index {
    color: grey;
    font-size: 0.8rem;
    width: 2rem;

    @include phone-only {
      display: none;
    }
  }

  .song-duration {
    font-size: 0.9rem;
    width: 5rem !important;

    text-align: left;
  }

  .options-icon {
    opacity: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    aspect-ratio: 1;
    width: 2rem;
    margin-right: 1rem;

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
