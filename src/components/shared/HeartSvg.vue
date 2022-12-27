<template>
  <button class="heart-button circular"><HeartSvg /></button>
</template>

<script setup lang="ts">
import HeartSvg from "@/assets/icons/heart.svg";
</script>

<style lang="scss">
.heart-button {
  $bg: rgb(247, 149, 149);
  background: $bg;
  align-items: center;
  padding: 0 1rem;
  gap: $smaller;

  &:hover {
    background: $bg;
  }
}
</style>
