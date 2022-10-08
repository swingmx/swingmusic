<template>
  <div class="hotkeys rounded-sm no-scroll">
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

import { default as NextSvg, default as PrevSvg } from "../../../assets/icons/next.svg";
import PauseSvg from "../../../assets/icons/pause.svg";
import PlaySvg from "../../../assets/icons/play.svg";

const q = useQStore();
</script>

<style lang="scss">
.hotkeys {
  display: grid;
  grid-template-columns: 4rem 4rem 4rem;
  height: 100%;

  button {
    height: 100%;
    padding: 0;
    background: none;
    border-radius: 0;

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
