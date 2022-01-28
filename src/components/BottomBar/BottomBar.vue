<template>
  <div class="b-bar border card-dark">
    <div class="grid">
      <SongCard />
      <div class="controlsx border rounded">
        <div class="controls controls-bottom">
          <HotKeys />
        </div>
        <div class="progress progress-bottom">
          <span class="durationx">0:45</span>
          <Progress />
          <span class="durationx">3:55</span>
        </div>
        <div class="r-group">
          <div class="heart image"></div>
          <div class="add-to image"></div>
          <div class="repeat image"></div>
        </div>
        <div class="controls controls-bottom"></div>
      </div>
      <div class="volume-group">

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import "../../assets/css/BottomBar/BottomBar.scss";
import playAudio from "../../composables/playAudio";
import SongCard from "./SongCard.vue";
import Progress from "../shared/Progress.vue";
import HotKeys from "../shared/HotKeys.vue";

const isPlaying = ref(playAudio.playing);

const { playNext } = playAudio;
const { playPrev } = playAudio;
const { playPause } = playAudio;
</script>
