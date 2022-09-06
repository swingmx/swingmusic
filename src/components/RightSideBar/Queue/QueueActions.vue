<template>
  <div class="queue-actions">
    <div class="left">
      <button class="clear-queue action" @click="queue.clearQueue">
        <ClearSvg />
        <span>Clear</span>
      </button>
      <button class="shuffle-queue action" @click="queue.shuffleQueue">
        <ShuffleSvg />
        <span>Shuffle</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import useQueueStore from "../../../stores/queue";

import ClearSvg from "@/assets/icons/delete.svg";
import ShuffleSvg from "@/assets/icons/shuffle.svg";

const queue = useQueueStore();
</script>

<style lang="scss">
.queue-actions {
  display: flex;
  justify-content: space-between;
  gap: $small;
  margin: 1rem;
  margin-bottom: 0;

  .left {
    display: flex;
    gap: $small;
  }

  .action {
    padding-left: $smaller;

    svg {
      transform: scale(0.8);
    }
  }
}
</style>
