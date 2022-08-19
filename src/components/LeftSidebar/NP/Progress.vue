<template>
  <input
    id="progress"
    type="range"
    :value="q.duration.current"
    min="0"
    :max="q.duration.full"
    step="0.1"
    @change="seek()"
    :style="{
      backgroundSize: `${
        (q.duration.current / (q.currenttrack.length || 0)) * 100
      }% 100%`,
    }"
  />
</template>

<script setup lang="ts">
import useQStore from "../../../stores/queue";

const q = useQStore();
const seek = () => {
  const elem = document.getElementById("progress") as HTMLInputElement;
  const value = elem.value;

  q.seek(value as unknown as number);
};
</script>
