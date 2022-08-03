<template>
  <div class="b-bar">
    <div class="grid rounded">
      <div class="controlsx rounded">
        <div class="controls-bottom">
          <HotKeys />
        </div>
        <div class="progress progress-bottom">
          <span class="durationx">{{ formatSeconds(q.track.current_time) }}</span>
          <Progress />
          <span class="durationx">{{ formatSeconds(q.length) }}</span>
        </div>
        <div class="r-group">
          <div id="heart" class="image ctrl-btn"></div>
          <div id="add-to" class="image ctrl-btn"></div>
          <div id="repeat" class="image ctrl-btn"></div>
        </div>
      </div>
      <div class="volume-group"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import "@/assets/scss/BottomBar/BottomBar.scss";
import { formatSeconds } from "@/composables/perks";
import HotKeys from "../LeftSidebar/NP/HotKeys.vue";
import Progress from "../LeftSidebar/NP/Progress.vue";

import useQStore from "@/stores/queue";

const q = useQStore();
</script>
