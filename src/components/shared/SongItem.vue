<template>
  <div
    class="songlist-item rounded"
    :class="[{ current: props.isCurrent }, { 'context-on': context_on }]"
    @dblclick="emitUpdate(props.song)"
    @contextmenu="showContextMenu"
  >
    <div class="index">{{ props.index }}</div>
    <div class="flex">
      <div
        class="album-art image rounded"
        :style="{
          backgroundImage: `url(&quot;${imguri + props.song.image}&quot;`,
        }"
        @click="emitUpdate(props.song)"
      >
        <div
          class="now-playing-track image"
          v-if="props.isPlaying && props.isCurrent"
          :class="{ active: isPlaying, not_active: !isPlaying }"
        ></div>
      </div>
      <div @click="emitUpdate(props.song)">
        <span class="ellip title">{{ props.song.title }}</span>
      </div>
    </div>
    <div class="song-artists">
      <div class="ellip" v-if="props.song.artists[0] !== ''">
        <span
          class="artist"
          v-for="artist in putCommas(props.song.artists)"
          :key="artist"
          >{{ artist }}</span
        >
      </div>
      <div class="ellip" v-else>
        <span class="artist">{{ props.song.albumartist }}</span>
      </div>
    </div>
    <router-link
      class="song-album ellip"
      :to="{
        name: 'AlbumView',
        params: {
          hash: props.song.albumhash,
        },
      }"
    >
      {{ props.song.album }}
    </router-link>
    <div class="song-duration">
      <div class="text">{{ formatSeconds(props.song.length) }}</div>
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
import { putCommas, formatSeconds } from "@/composables/perks";
import useContextStore from "@/stores/context";
import useModalStore from "@/stores/modal";
import useQueueStore from "@/stores/queue";
import { ContextSrc } from "@/composables/enums";
import OptionSvg from "@/assets/icons/more.svg";

import { ref } from "vue";
import trackContext from "@/contexts/track_context";
import { Track } from "@/interfaces";
import { paths } from "@/config";

const contextStore = useContextStore();

const context_on = ref(false);
const imguri = paths.images.thumb;
const options_button_clicked = ref(false);

const showContextMenu = (e: Event) => {
  e.preventDefault();
  e.stopPropagation();

  const menus = trackContext(props.song, useModalStore, useQueueStore);

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
  song: Track;
  index: Number;
  isPlaying: Boolean;
  isCurrent: Boolean;
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
    text-transform: capitalize;
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
    text-align: center;
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
    padding-left: 4rem;
    align-items: center;

    .album-art {
      position: absolute;
      left: $small;
      width: 3rem;
      height: 3rem;
      margin-right: 1rem;
      display: grid;
      place-items: center;
      cursor: pointer;
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
