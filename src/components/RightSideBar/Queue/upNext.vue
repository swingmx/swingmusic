<template>
  <div class="bottom-left">
    <div class="upNext rounded-sm border" title="play next song">
      <img
        :src="paths.images.thumb.small + queue.next?.image"
        class="rounded-sm"
      />
      <div class="text">
        <div class="title"><b>Stiff necked fools</b></div>
        <div class="from">Next up</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { paths } from "@/config";
import useQueueStore from "@/stores/queue";

import { ref } from "vue";

const context_on = ref(false);
const queue = useQueueStore();
</script>

<style lang="scss">
.bottom-left {
  overflow: hidden;
  display: grid;
  padding-top: 2px;
  // place-content: end;

  .upNext {
    padding: $smaller;
    grid-template-columns: max-content 1fr;
    gap: $small;
    display: grid;
    width: 20rem;
    background-color: rgba(255, 255, 255, 0.048);
    cursor: pointer;

    &:hover {
      transition: all 0.25s ease;
      background-color: $gray4;
    }

    img {
      height: 2.75rem;
    }

    .text {
      font-size: small;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;

      .from {
        opacity: 0.75;
        font-size: $medium;
        margin-top: $smaller;
      }
    }
  }
}
</style>
