<template>
  <div class="play-btn rounded shadow-sm" @click="playThis"></div>
</template>
<script setup lang="ts">
function playThis(e: Event) {
  e.preventDefault();
  e.stopImmediatePropagation();
}
</script>
<style lang="scss">
.play-btn {
  width: 2.5rem;
  height: 2.5rem;
  background-color: $gray3;
  background-image: url("../../assets/icons/play.svg");
  background-size: 1.75rem;
  background-position: 50% 50%;
  transition: all 0.25s ease-in-out;

  &:hover {
    background-color: $accent;
    transform: scale(1.1);
  }
}
</style>
