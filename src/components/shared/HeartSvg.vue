<template>
  <button class="heart-button circular" @click="emit('handleFav')">
    <HeartFillSvg v-if="state" />
    <HeartSvg v-else />
  </button>
</template>

<script setup lang="ts">
import HeartSvg from "@/assets/icons/heart.svg";
import HeartFillSvg from "@/assets/icons/heart.fill.svg";

defineProps<{
  state: boolean | undefined;
}>();

const emit = defineEmits<{
  (event: "handleFav"): void;
}>();
</script>

<style lang="scss">
.heart-button {
  $bg: rgb(255, 184, 184);
  background: $bg;
  align-items: center;
  padding: 0 1rem;
  gap: $smaller;

  &:hover {
    background: $bg;
  }
}
</style>
