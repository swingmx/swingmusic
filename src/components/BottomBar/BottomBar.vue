<template>
  <div class="b-bar bg-black pad-medium rounded">
    <div class="info">
      <img
        :src="paths.images.thumb + queue.currenttrack?.image"
        alt=""
        class="rounded shadow-lg"
      />
      <div class="tags">
        <div class="np-artist ellip">
          <span
            v-for="artist in putCommas(
              queue.currenttrack?.artists || ['Artist']
            )"
          >
            {{ artist }}
          </span>
        </div>
        <div class="np-title ellip">
          {{ queue.currenttrack?.title || "Track title" }}
        </div>
      </div>
    </div>
    <Progress />
    <!-- <div class="ex-hotkeys">
      <HotKeys />
    </div> -->
    <div class="time">
      <span class="current">{{ formatSeconds(queue.currentTime) }}</span>
      <HotKeys />
      <span class="full">{{
        formatSeconds(queue.fullTime || queue.currenttrack.length)
      }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import "@/assets/scss/BottomBar/BottomBar.scss";
import { formatSeconds, putCommas } from "@/utils";
import HotKeys from "../LeftSidebar/NP/HotKeys.vue";
import Progress from "../LeftSidebar/NP/Progress.vue";

import { paths } from "@/config";
import useQStore from "@/stores/queue";

const queue = useQStore();
</script>

<style lang="scss">
.b-bar {
  display: grid;
  grid-template-rows: 1fr max-content;
  gap: 1rem;
  padding: 1rem;
  padding-bottom: 1rem;
  position: relative;

  .time {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    align-items: center;

    .full {
      text-align: end;
    }
  }

  .ex-hotkeys {
    position: absolute;
    width: 10rem;
    right: 1rem;
    top: 1rem;
    border-radius: $small;
  }

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
      gap: $smaller;

      .np-title {
        font-size: 1.15rem;
        font-weight: bold;
      }

      .np-artist {
        opacity: 0.75;
        font-size: 0.9rem;
      }
    }
  }
}
</style>
