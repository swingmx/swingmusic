<template>
  <div
    class="track-item"
    @click="playThis(track)"
    :class="[
      {
        currentInQueue: isCurrent,
      },
      { contexton: context_on },
    ]"
    @contextmenu.prevent="showMenu"
  >
    <div class="album-art">
      <img :src="paths.images.thumb.small + track.image" class="rounded-sm" />
      <div
        class="now-playing-track-indicator image"
        v-if="isCurrent"
        :class="{ last_played: !isCurrentPlaying }"
      ></div>
    </div>
    <div class="tags">
      <div class="title ellip" v-tooltip>
        {{ track.title }}
      </div>
      <hr />
      <div class="artist">
        <ArtistName
          :artists="track.artist"
          :albumartists="track.albumartist"
          :smaller="true"
        />
      </div>
    </div>
    <div
      class="remove-track flex"
      @click.stop="queue.removeFromQueue(index)"
      v-if="isQueueTrack"
    >
      <div title="remove from queue" >
        <DelSvg/>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import DelSvg from "@/assets/icons/plus.svg";
import { showTrackContextMenu as showContext } from "@/composables/context";
import { paths } from "@/config";
import { Track } from "@/interfaces";
import useQueueStore from "@/stores/queue";
import ArtistName from "./ArtistName.vue";

const props = defineProps<{
  track: Track;
  isCurrent: boolean;
  isCurrentPlaying: boolean;
  isQueueTrack?: boolean;
  index?: number;
}>();

const queue = useQueueStore();
const context_on = ref(false);

function showMenu(e: MouseEvent) {
  showContext(e, props.track, context_on);
}

const emit = defineEmits<{
  (e: "playThis"): void;
}>();

const playThis = (track: Track) => {
  emit("playThis");
};
</script>

<style lang="scss">
.currentInQueue {
  background-color: $gray4;
}

.contexton {
  background-color: $gray4;
  color: $white !important;
}

.track-item {
  display: grid;
  grid-template-columns: min-content 1fr max-content;
  align-items: center;
  padding: $small 1rem;

  .tags {
    .title {
      width: fit-content;
    }
  }

  .remove-track {
    opacity: 0;
    transition: all 0.25s ease;
    transform: scale(0.75) translateY(1rem) rotate(45deg);

    &:hover {
      opacity: 1 !important;
    }
  }

  &:hover {
    .remove-track {
      opacity: 0.5;
      transform: scale(1) translateY(0) rotate(45deg);
    }

    background-color: $gray5;
  }

  hr {
    border: none;
    margin: 0.1rem;
  }

  .album-art {
    display: flex;
    align-items: center;
    justify-content: center;

    margin-right: $small;
    position: relative;

    .now-playing-track-indicator {
      position: absolute;
    }
  }

  img {
    width: 3rem;
    height: 3rem;
  }

  .artist {
    opacity: 0.67;
    width: fit-content;
  }
}
</style>
