<template>
  <div class="b-bar border card-dark">
    <div class="grid">
      <SongCard :collapsed="props.collapsed" />
      <div class="controlsx rounded">
        <div class="controls controls-bottom">
          <HotKeys />
        </div>
        <div class="progress progress-bottom">
          <span class="durationx">{{ formatSeconds(current_pos) }}</span>
          <Progress />
          <span class="durationx">{{
            formatSeconds(state.current.value.length)
          }}</span>
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
import perks from "../../composables/perks";
import playAudio from "../../composables/playAudio";

const current_pos = playAudio.current_time
const formatSeconds = perks.formatSeconds;

const props = defineProps({
  collapsed: {
    type: Boolean,
    default: false,
  },
});
</script>
