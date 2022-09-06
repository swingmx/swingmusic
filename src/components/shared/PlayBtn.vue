<template>
  <button
    class="play-btn rounded-md"
    @click="usePlayFrom(source, useQStore, store)"
  >
    <PlaySvg />
  </button>
</template>

<script setup lang="ts">
import { playSources } from "@/composables/enums";
import useAlbumStore from "@/stores/pages/album";
import usePlaylistStore from "@/stores/pages/playlist";
import usePlayFrom from "@/composables/usePlayFrom";
import useQStore from "@/stores/queue";

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
}
</style>
