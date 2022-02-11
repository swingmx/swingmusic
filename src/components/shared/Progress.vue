<template>
  <input
    class="progress-bar"
    id="progress"
    type="range"
    :value="pos"
    min="0"
    max="1000"
    @change="seek()"
  />
</template>

<script setup>
import { ref } from "vue";
import playAudio from "../../composables/playAudio";
const pos = ref(playAudio.pos);

const seek = () => {
  playAudio.seek(document.getElementById("progress").value);
};
</script>
