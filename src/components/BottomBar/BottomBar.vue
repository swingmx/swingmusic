<template>
  <div class="b-bar border card-dark">
    <div class="grid">
      <SongCard />
      <div class="controlsx">
        <div class="controls controls-bottom">
          <div class="nav">
            <div class="image" id="previous" @click="playPrev"></div>
            <div
              class="image play-pause"
              @click="playPause"
              :class="{ isPlaying: isPlaying }"
            ></div>
            <div class="image" id="next" @click="playNext"></div>
          </div>
        </div>
        <div class="progress progress-bottom">
          <span class="durationx">0:45</span>
          <input
            id="progress"
            type="range"
            :value="pos"
            min="0"
            max="1000"
            @change="seek()"
          />
          <span class="durationx">3:55</span>
        </div>
      </div>
      <div class="prog"></div>
      <div class="volume-group"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import "../../assets/css/BottomBar/BottomBar.scss";
import playAudio from "../../composables/playAudio";
import SongCard from "./SongCard.vue";

const pos = ref(playAudio.pos);
const isPlaying = ref(playAudio.playing);

const seek = () => {
  playAudio.seek(document.getElementById("progress").value);
};

const { playNext } = playAudio;
const { playPrev } = playAudio;
const { playPause } = playAudio;
</script>
