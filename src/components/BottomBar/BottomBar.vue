<template>
  <div class="b-bar bg-black pad-medium rounded">
    <div class="info">
      <img
        :src="paths.images.thumb + queue.currenttrack?.image"
        alt=""
        class="rounded"
      />
      <div class="tags">
        <div class="np-artist ellip">
          <span v-for="artist in putCommas(queue.currenttrack?.artists || ['Artist'])">
            {{ artist }}
          </span>
        </div>
        <div class="np-title ellip">
          {{ queue.currenttrack?.title || "Track title" }}
        </div>
      </div>
    </div>
    <Progress />
  </div>
</template>

<script setup lang="ts">
import "@/assets/scss/BottomBar/BottomBar.scss";
import { formatSeconds, putCommas } from "@/utils";
import Progress from "../LeftSidebar/NP/Progress.vue";

import useQStore from "@/stores/queue";
import { paths } from "@/config";

const queue = useQStore();
</script>

<style lang="scss">
.b-bar {
  display: grid;
  grid-template-rows: 1fr max-content;
  border-radius: 1rem;
  gap: 1rem;
  padding: 1rem;
  padding-bottom: 2rem;

  .info {
    display: grid;
    grid-template-columns: max-content 1fr;
    gap: 1rem;

    img {
      height: 6rem;
      width: auto;
    }

    .tags {
      display: flex;
      flex-direction: column;
      justify-content: flex-end;

      .np-title {
        font-size: 1.15rem;
        font-weight: bold;
        margin-bottom: $small;
      }

      .np-artist {
        opacity: 0.75;
        font-size: 0.9rem;
      }
    }
  }
}
</style>
