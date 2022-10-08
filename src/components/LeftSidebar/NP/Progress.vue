<template>
  <input
    id="progress"
    type="range"
    :value="time.current"
    min="0"
    :max="time.full"
    step="0.1"
    @change="seek()"
    :style="{
      backgroundSize: `${
        (time.current / (q.currenttrack?.duration || 0)) * 100
      }% 100%`,
    }"
  />
</template>

<script setup lang="ts">
import useQStore from "@/stores/queue";

const q = useQStore();

const { duration: time } = q;
const seek = () => {
  const elem = document.getElementById("progress") as HTMLInputElement;
  const value = elem.value;

  q.seek(value as unknown as number);
};
</script>
