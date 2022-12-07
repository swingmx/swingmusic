<template>
  <button class="play-btn circular shadow-sm" @click.prevent.stop="handlePlay">
    <PlaySvg />
  </button>
</template>

<script setup lang="ts">
import useQStore from "@/stores/queue";
import useAlbumStore from "@/stores/pages/album";
import usePlaylistStore from "@/stores/pages/playlist";

import { playSources } from "@/composables/enums";
import usePlayFrom from "@/composables/usePlayFrom";

import PlaySvg from "../../assets/icons/play.svg";
import { playFromAlbumCard } from "@/composables/usePlayFrom";

const props = defineProps<{
  source: playSources;
  albumHash?: string;
  albumName?: string;
  store: typeof useAlbumStore | typeof usePlaylistStore;
}>();

function handlePlay() {
  switch (props.source) {
    case playSources.album:
      playFromAlbumCard(
        useQStore,
        props.albumHash || "",
        props.albumName || ""
      );
      break;

    default:
      break;
  }
}
</script>

<style lang="scss">
.play-btn {
  aspect-ratio: 1;
  padding: 0;
  background: $black;

  svg {
    transition: none;
  }
}
</style>
