<template>
  <div class="hotkeys">
    <div class="image ctrl-btn" id="previous" @click="props.prev"></div>
    <div
      class="image ctrl-btn play-pause"
      @click="playPause"
      :class="{ isPlaying: props.playing }"
    ></div>
    <div class="image ctrl-btn" id="next" @click="props.next"></div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  playing: boolean;
  playPause: () => void;
  next: () => void;
  prev: () => void;
}>();
</script>

<style lang="scss">
.hotkeys {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  width: 100%;
  gap: $small;
  height: 3rem;
  align-items: center;
  place-content: flex-end;

  .ctrl-btn {
    height: 2.5rem;
    width: 100%;
    background-size: 1.5rem !important;
    cursor: pointer;
    border-radius: 0.5rem;

    &:hover {
      background-color: $red;
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
