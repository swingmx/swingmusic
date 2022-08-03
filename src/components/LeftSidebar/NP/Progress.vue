<template>
  <input
    id="progress"
    type="range"
    :value="q.duration.current"
    min="0"
    :max="q.duration.full"
    step="0.1"
    @change="seek()"
  />
</template>

<script setup lang="ts">
import useQStore from "../../../stores/queue";

const q = useQStore();
const seek = () => {
  const elem = <HTMLFormElement>document.getElementById("progress");
  const value = elem.value;

  q.seek(value);
};
</script>
