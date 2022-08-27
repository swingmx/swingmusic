<template>
  <div class="switch rounded" :class="{ toggled: state }">
    <div class="circle circular"></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

defineProps<{
  state: boolean;
}>();
</script>

<style lang="scss">
.switch {
  height: 2rem;
  background-color: $gray;
  width: 3.75rem;
  padding: $smaller;
  position: relative;
  transition: all 0.25s ease;

  .circle {
    transition: all 0.25s ease;
    height: 1.5rem;
    aspect-ratio: 1;
    background-color: $gray1;
    position: absolute;
    left: $smaller;
  }
}

.toggled {
  background-color: $darkestblue;
  transition-delay: 0.15s;

  .circle {
    background-color: $white;
    left: calc((100% - ($smaller + 1.5rem)));
  }
}
</style>
