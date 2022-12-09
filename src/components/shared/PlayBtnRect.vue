<template>
  <button class="playbtnrect shadow-sm" @click="usePlayFrom(source, useQStore, store)">
    <playBtnSvg />
    <div class="text">Play</div>
  </button>
</template>

<script setup lang="ts">
import { playSources } from "@/composables/enums";
import usePlayFrom from "@/composables/usePlayFrom";
import useFStore from "@/stores/pages/folder";
import useAStore from "@/stores/pages/album";
import usePStore from "@/stores/pages/playlist";
import useArtistPageStore from "@/stores/pages/artist";
import useQStore from "@/stores/queue";
import playBtnSvg from "@/assets/icons/play.svg";

defineProps<{
  source: playSources;
  store:
    | typeof useQStore
    | typeof useFStore
    | typeof useAStore
    | typeof usePStore
    | typeof useArtistPageStore;
}>();
</script>

<style lang="scss">
.playbtnrect {
  width: 6rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.5s ease-in-out;
  color: $white;
  background: $darkestblue !important;
  border-radius: 2rem;
}
</style>
