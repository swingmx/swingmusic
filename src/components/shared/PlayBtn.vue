<template>
  <button
    class="play-btn circular"
    @click.prevent.stop="usePlayFrom(source, useQStore, store)"
  >
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
  color: string;
}>();
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
