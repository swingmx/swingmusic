<template>
  <div class="now-playing-card t-center rounded">
    <SongCard :track="queue.currenttrack" />
    <div class="l-track-time">
      <span class="rounded">{{ formatSeconds(duration.current) }}</span>
      <!-- <HeartSvg /> -->
      <span class="rounded">{{ formatSeconds(duration.full) }}</span>
    </div>
    <Progress />
    <HotKeys />
  </div>
</template>

<script setup lang="ts">
import useQStore from "../../stores/queue";
import { formatSeconds } from "@/utils";

import HotKeys from "./NP/HotKeys.vue";
import Progress from "./NP/Progress.vue";
import SongCard from "./NP/SongCard.vue";

const queue = useQStore();
const { duration } = queue;
</script>
<style lang="scss">
.now-playing-card {
  padding: 1rem;
  width: 100%;
  display: grid;
  grid-template-rows: 1fr max-content max-content max-content;
  gap: 1rem;

  .l-track-time {
    display: flex;
    justify-content: space-between;
    opacity: 0.8;

    span {
      font-size: small;
      padding: $smaller;
    }
  }

  &:hover {
    ::-moz-range-thumb {
      height: 0.8rem;
    }

    ::-webkit-slider-thumb {
      height: 0.8rem;
    }

    ::-ms-thumb {
      height: 0.8rem;
    }
  }

  .context_on {
    background-color: $accent;
  }

  .menu {
    right: $small;
    transform: rotate(90deg);
  }
}
</style>
