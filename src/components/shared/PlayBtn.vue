<template>
  <button class="play-btn" @click="usePlayFrom(source, useQStore, store)">
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

defineProps<{
  source: playSources;
  store: typeof useAlbumStore | typeof usePlaylistStore;
}>();
</script>

<style lang="scss">
.play-btn {
  aspect-ratio: 1;
  padding: 0;
  border-radius: 0.65rem;

  svg {
    transition: none;
  }
}
</style>
