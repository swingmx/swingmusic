<template>
  <div class="switch rounded" :class="{ toggled: state }">
    <div class="circle circular"></div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  state: boolean;
}>();
</script>

<style lang="scss">
.switch {
  height: 1.5rem;
  background-color: $gray3;
  width: 2.5rem;
  padding: $smaller;
  position: relative;
  transition: all 0.25s ease;

  .circle {
    transition: all 0.25s ease;
    height: 1rem;
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
    left: calc((100% - ($smaller + 1rem)));
  }
}
</style>
