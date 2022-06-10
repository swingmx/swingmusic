<template>
  <div
    class="play-btn rounded shadow-sm"
    @click="usePlayFrom(source, useQStore, store)"
  ></div>
</template>

<script setup lang="ts">
import { playSources } from "@/composables/enums";
import useAlbumStore from "@/stores/pages/album";
import usePlaylistStore from "@/stores/pages/playlist";
import usePlayFrom from "@/composables/usePlayFrom";
import useQStore from "@/stores/queue";

defineProps<{
  source: playSources;
  store: typeof useAlbumStore | typeof usePlaylistStore;
}>();
</script>
<style lang="scss">
.play-btn {
  height: 2.25rem;
  background-color: $gray3;
  background-image: url("../../assets/icons/play.svg");
  background-size: 1.75rem;
  background-repeat: no-repeat;
  background-position: 50% 50%;
  transition: all 0.25s ease-in-out;
  aspect-ratio: 1;

  &:hover {
    background-color: $accent;
  }
}
</style>
