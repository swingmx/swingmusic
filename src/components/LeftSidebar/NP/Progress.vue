<template>
  <input
    id="progress"
    type="range"
    :value="props.pos"
    min="0"
    max="100"
    step="0.1"
    @change="seek()"
  />
</template>

<script setup lang="ts">
const seek = () => {
  const value = Number(document.getElementById("progress").value);
  props.seek(value);
};

const props = defineProps<{
  pos: number;
  seek: (time: number) => void;
}>();
</script>
