<template>
  <div class="hotkeys rounded-sm noscroll">
    <button @click.prevent="q.playPrev">
      <PrevSvg />
    </button>
    <button v-auto-animate @click.prevent="q.playPause">
      <PauseSvg v-if="q.playing" />
      <PlaySvg v-else />
    </button>
    <button @click.prevent="q.playNext">
      <NextSvg />
    </button>
  </div>
</template>

<script setup lang="ts">
import useQStore from "@/stores/queue";

import NextSvg from "../../../assets/icons/next.svg";
import PrevSvg from "../../../assets/icons/next.svg";
import PauseSvg from "../../../assets/icons/pause.svg";
import PlaySvg from "../../../assets/icons/play.svg";

const q = useQStore();
</script>

<style lang="scss">
.hotkeys {
  display: grid;
  grid-template-columns: 2rem 4rem 2rem;
  gap: 1rem;
  width: 100%;

  button {
    height: 2rem;
    padding: 0;
    background: none;

    &:hover {
      background: $darkestblue;
    }
  }

  button:first-child {
    svg {
      transform: rotate(180deg);
    }
  }
}
</style>
