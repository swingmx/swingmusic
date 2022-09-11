<template>
  <div class="b-bar bg-primary pad-medium rounded" v-if="settings.show_alt_np">
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
              queue.currenttrack?.artists || ['♥ Hello ♥']
            )"
          >
            {{ artist }}
          </span>
        </div>
        <div class="np-title ellip">
          {{ queue.currenttrack?.title || "Play something"}}
        </div>
      </div>
    </div>
    <Progress />
    <div class="time">
      <span class="current">{{ formatSeconds(queue.duration.current) }}</span>
      <HotKeys />
      <span class="full">{{
        formatSeconds(queue.currenttrack ? queue.currenttrack.length : 0)
      }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import "@/assets/scss/BottomBar/BottomBar.scss";
import useSettingsStore from "@/stores/settings";
import { formatSeconds, putCommas } from "@/utils";
import HotKeys from "../LeftSidebar/NP/HotKeys.vue";
import Progress from "../LeftSidebar/NP/Progress.vue";

import { paths } from "@/config";
import useQStore from "@/stores/queue";

const queue = useQStore();
const settings = useSettingsStore();
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
