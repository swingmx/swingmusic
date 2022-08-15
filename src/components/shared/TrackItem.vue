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
      <img :src="paths.images.thumb + track.image" alt="" class="rounded" />
      <div
        class="now-playing-track-indicator image"
        v-if="isCurrent"
        :class="{ last_played: !isPlaying }"
      ></div>
    </div>
    <div class="tags">
      <div class="title ellip">
        {{ track.title }}
      </div>
      <hr />
      <div class="artist">
        <div class="ellip" v-if="track.artists[0] !== ''">
          <span v-for="artist in putCommas(track.artists)" :key="artist">{{
            artist
          }}</span>
        </div>
        <div class="ellip" v-else>
          <span>{{ track.albumartist }}</span>
        </div>
      </div>
    </div>
    <div
      class="remove-track flex"
      @click.stop="queue.removeFromQueue(index)"
      v-if="isQueueTrack"
    >
      <DelSvg />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import { paths } from "@/config";
import { putCommas } from "@/utils";
import { Track } from "@/interfaces";
import { showTrackContextMenu as showContext } from "@/composables/context";
import DelSvg from "@/assets/icons/plus.svg";
import useQueueStore from "@/stores/queue";

const props = defineProps<{
  track: Track;
  isCurrent: boolean;
  isPlaying: boolean;
  isQueueTrack?: boolean;
  index?: number;
}>();

const queue = useQueueStore();
const context_on = ref(false);

function showMenu(e: Event) {
  showContext(e, props.track, context_on);
}

const emit = defineEmits<{
  (e: "PlayThis"): void;
}>();

const playThis = (track: Track) => {
  emit("PlayThis");
};
</script>

<style lang="scss">
.currentInQueue {
  background: linear-gradient(37deg, $gray4, $gray3, $gray3);
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

  .remove-track {
    opacity: 0;
    transition: all 0.25s ease;
    transform: translateX(1rem) rotate(45deg);

    &:hover {
      opacity: 1 !important;
    }
  }

  &:hover {
    .remove-track {
      opacity: 0.5;
      transform: translateX(0) rotate(45deg);
    }

    cursor: pointer;
    background: linear-gradient(37deg, $gray4, $gray3, $gray3);
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

  .title {
    word-break: break-all;
  }

  .artist {
    word-break: break-all;
    font-size: small;
    color: rgba(255, 255, 255, 0.637);
  }
}
</style>
