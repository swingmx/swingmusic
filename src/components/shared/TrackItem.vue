<template>
  <div
    class="track-item"
    @click="playThis(props.track)"
    :class="[
      {
        currentInQueue: props.isCurrent,
      },
      { contexton: context_on },
    ]"
    @contextmenu.prevent="showMenu"
  >
    <div class="album-art">
      <img :src="paths.images.thumb + track.image" alt="" class="rounded" />
      <div
        class="now-playing-track-indicator image"
        v-if="props.isCurrent"
        :class="{ last_played: !props.isPlaying }"
      ></div>
    </div>
    <div class="tags">
      <div class="title ellip">
        {{ props.track.title }}
      </div>
      <hr />
      <div class="artist ellip">
        <span v-for="artist in putCommas(props.track.artists)" :key="artist">{{
          artist
        }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import { paths } from "@/config";
import { putCommas } from "@/utils";
import { Track } from "@/interfaces";
import { showTrackContextMenu as showContext } from "@/composables/context";

const props = defineProps<{
  track: Track;
  isCurrent: boolean;
  isPlaying: boolean;
}>();

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
  grid-template-columns: min-content 1fr;
  align-items: center;
  padding: $small 1rem;

  &:hover {
    cursor: pointer;
    background: linear-gradient(37deg, $gray4, $gray3, $gray3);
  }

  hr {
    border: none;
    margin: 0.1rem;
  }

  // .tags {
  //   border: solid 1px;
  // }

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
