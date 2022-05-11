<template>
  <div class="l_ rounded">
    <div class="headin">Now Playing</div>
    <div class="button menu image rounded"></div>
    <div class="separator no-border"></div>
    <div>
      <SongCard :track="queue.current" />
      <Progress :seek="queue.seek" :pos="queue.current_time" />
      <HotKeys
        :playing="queue.playing"
        :playPause="queue.playPause"
        :next="queue.playNext"
        :prev="queue.playPrev"
      />
    </div>
  </div>
</template>

<script setup>
import SongCard from "./SongCard.vue";
import HotKeys from "./NP/HotKeys.vue";
import Progress from "./NP/Progress.vue";
import useQStore from "../../stores/queue";

const queue = useQStore();
</script>
<style lang="scss">
.l_ {
  padding: 1rem;
  background-color: $primary;
  margin: $small;
  text-align: center;
  width: 14rem;
  display: grid;
  position: relative;
  text-transform: capitalize;

  &:hover {
    ::-moz-range-thumb {
      height: 0.8rem;
    }

    ::-webkit-slider-thumb {
      height: 0.8rem;
    }

    ::-ms-thumb {
      height: 0.8rem;
    }
  }

  .headin {
    font-weight: bold;
    font-size: 0.9rem;
  }

  .button {
    height: 2rem;
    width: 2rem;
    position: absolute;
    background-size: 1.5rem;
    top: $small;
    cursor: pointer;
    transition: all 200ms;

    &:hover {
      background-color: $gray2;
    }
  }

  .menu {
    right: $small;
    background-image: url("../../assets/icons/right-arrow.svg");
    transform: rotate(90deg);

    &:hover {
      transform: rotate(0deg);
    }
  }

  br {
    height: 0rem;
  }

  .art {
    width: 100%;
    display: grid;
    place-items: center;
    margin-bottom: $small;

    .l-image {
      height: 12rem;
      width: 12rem;
    }
  }

  #bitrate {
    position: absolute;
    font-size: 0.75rem;
    width: max-content;
    padding: 0.2rem 0.35rem;
    top: 13.25rem;
    left: 1.5rem;
    background-color: $black;
    border-radius: $smaller;
    box-shadow: 0rem 0rem 1rem rgba(0, 0, 0, 0.438);
  }

  .title {
    font-weight: 900;
  }

  .artists {
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.808);

    &:hover {
      text-decoration: underline 1px !important;
    }
  }
}
</style>
