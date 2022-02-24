<template>
  <input
    id="progress"
    type="range"
    :value="pos"
    min="0"
    max="100"
    step="0.1"
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
