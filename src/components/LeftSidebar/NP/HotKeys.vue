<template>
  
  <div class="hotkeys">
    <div class="image ctrl-btn" id="previous" @click="q.playPrev"></div>
    <div
      class="image ctrl-btn play-pause"
      @click="q.playPause"
      :class="{ isPlaying: q.playing }"
    ></div>
    <div class="image ctrl-btn" id="next" @click="q.playNext"></div>
  </div>
</template>

<script setup lang="ts">
import useQStore from "@/stores/queue";

const q = useQStore();
</script>

<style lang="scss">

.hotkeys {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $small;
  height: 2.5rem;
  align-items: center;
  justify-content: center;
  place-content: flex-end;
  width: 100%;

  .ctrl-btn {
    height: 2.5rem;
    width: 100%;
    background-size: 1.5rem !important;
    cursor: pointer;
    border-radius: 0.5rem;

    &:hover {
      background-color: $accent;
    }
  }

  #previous {
    background-image: url(../../../assets/icons/previous.svg);
  }

  .play-pause {
    background-image: url(../../../assets/icons/play.svg);
  }

  .isPlaying {
    background-image: url(../../../assets/icons/pause.svg);
  }

  #next {
    background-image: url(../../../assets/icons/next.svg);
  }
}
</style>
