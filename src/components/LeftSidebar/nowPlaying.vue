<template>
  <div class="now-playing-card t-center rounded">
    <div>
      <SongCard :track="currenttrack" />
      <div class="l-track-time">
        <span class="rounded">{{ formatSeconds(duration.current) }}</span
        ><span class="rounded">{{ formatSeconds(duration.full) }}</span>
      </div>
      <Progress />
    </div>
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
const { currenttrack, duration } = queue;
</script>
<style lang="scss">
.now-playing-card {
  padding: 1rem;
  width: 100%;
  display: grid;
  grid-template-rows: 1fr max-content;
  position: relative;
  gap: 1rem;

  .l-track-time {
    display: flex;
    justify-content: space-between;
    opacity: 0.8;
    margin-top: $small;

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
