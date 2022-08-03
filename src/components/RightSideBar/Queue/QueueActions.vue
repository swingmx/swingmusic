<template>
  <div class="queue-actions">
    <div class="left">
      <button class="clear-queue action" @click="queue.clearQueue">
        <ClearSvg />
        <span>Clear</span>
      </button>
      <button class="shuffle-queue action">
        <SaveAsPlaylistSvg />
        <span> Save as Playlist </span>
      </button>
    </div>
    <div class="right">
      <button class="more-action action">
        <MoreSvg />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import useQueueStore from "../../../stores/queue";

import ClearSvg from "@/assets/icons/delete.svg";
import SaveAsPlaylistSvg from "@/assets/icons/sdcard.svg";
import MoreSvg from "@/assets/icons/more.svg";

const queue = useQueueStore();
</script>

<style lang="scss">
.queue-actions {
  display: flex;
  justify-content: space-between;
  gap: $small;
  margin: 1rem;
  margin-bottom: 0;

  .action {
    padding: $smaller;
    padding-right: $small;

    svg {
      transform: scale(0.8);
    }
  }

  .more-action {
    padding-right: $smaller;
    svg {
      transform: scale(1.25);
    }
  }
}
</style>
