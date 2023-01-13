<!-- Track component used in the right sidebar -->
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
    <div class="float-buttons flex">
      <div
        :title="is_fav ? 'Add to favorites' : 'Remove from favorites'"
        @click.stop="() => addToFav(track.trackhash)"
      >
        <HeartSvg :state="is_fav" :no_emit="true" />
      </div>
      <div
        v-if="isQueueTrack"
        class="remove-track"
        title="remove from queue"
        @click.stop="queue.removeFromQueue(index)"
      >
        <DelSvg />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";

import DelSvg from "@/assets/icons/plus.svg";
import { showTrackContextMenu as showContext } from "@/composables/context";
import { paths } from "@/config";
import { Track } from "@/interfaces";
import useQueueStore from "@/stores/queue";
import ArtistName from "./ArtistName.vue";
import HeartSvg from "./HeartSvg.vue";
import favoriteHandler from "@/composables/favoriteHandler";
import { favType } from "@/composables/enums";

const props = defineProps<{
  track: Track;
  isCurrent: boolean;
  isCurrentPlaying: boolean;
  isQueueTrack?: boolean;
  index?: number;
}>();

const queue = useQueueStore();
const context_on = ref(false);
const is_fav = ref(props.track.is_favorite);

function showMenu(e: MouseEvent) {
  showContext(e, props.track, context_on);
}

const emit = defineEmits<{
  (e: "playThis"): void;
}>();

const playThis = (track: Track) => {
  emit("playThis");
};

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

  .float-buttons {
    opacity: 0;

    .heart-button {
      width: 2rem;
      padding: 0;
      border: none;
      transition: all 0.25s ease;
      transform: scale(1) translateY(-1rem);
    }

    .remove-track {
      margin-top: $smaller;
      transition: all 0.25s ease;
      transform: scale(1) translateY(1rem) rotate(45deg);
    }

    &:hover {
      opacity: 1 !important;
    }
  }

  &:hover {
    .float-buttons {
      opacity: 1;
    }

    .heart-button {
      transform: scale(1) translateY(0);
    }

    .remove-track {
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
