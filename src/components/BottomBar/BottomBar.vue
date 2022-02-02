<template>
  <div class="b-bar border card-dark">
    <div class="grid">
      <SongCard/>
      <div class="controlsx border rounded">
        <div class="controls controls-bottom">
          <HotKeys />
        </div>
        <div class="progress progress-bottom">
          <span class="durationx">0:45</span>
          <Progress />
          <span class="durationx">{{ state.current.value.length }}</span>
        </div>
        <div class="r-group">
          <div class="heart image"></div>
          <div class="add-to image"></div>
          <div class="repeat image"></div>
        </div>
        <div class="controls controls-bottom"></div>
      </div>
      <div class="volume-group"></div>
    </div>
  </div>
</template>

<script setup>
import "../../assets/css/BottomBar/BottomBar.scss";
import SongCard from "./SongCard.vue";
import Progress from "../shared/Progress.vue";
import HotKeys from "../shared/HotKeys.vue";
import state from "../../composables/state";
</script>
