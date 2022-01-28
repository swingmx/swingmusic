<template>
  <div class="nav">
    <div class="image" id="previous" @click="playPrev"></div>
    <div
      class="image play-pause"
      @click="playPause"
      :class="{ isPlaying: isPlaying }"
    ></div>
    <div class="image" id="next" @click="playNext"></div>
  </div>
</template>

<script setup>
import playAudio from "../../composables/playAudio";

const playPause = playAudio.playPause;
const playNext = playAudio.playNext;
const playPrev = playAudio.playPrev;

const isPlaying = playAudio.playing;
</script>

<style lang="scss">
.nav {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  width: 100%;
  gap: $small;

  & * {
    height: 2rem;
    width: 2rem;
    background-size: 1.2rem !important;
    cursor: pointer;
    border-radius: 0.5rem;

    &:hover {
      background-color: $pink;
    }
  }

  #previous {
    background-image: url(../../assets/icons/previous.svg);
  }

  .play-pause {
    background-image: url(../../assets/icons/play.svg);
  }

  .isPlaying {
    background-image: url(../../assets/icons/pause.svg);
  }

  #next {
    background-image: url(../../assets/icons/next.svg);
  }
}
</style>
