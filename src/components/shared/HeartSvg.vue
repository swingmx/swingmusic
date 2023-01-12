<template>
  <button
    class="heart-button circular"
    @click="!no_emit && emit('handleFav')"
    :class="{
      is_fav: state,
    }"
  >
    <HeartFillSvg v-if="state" />
    <HeartSvg v-else />
  </button>
</template>

<script setup lang="ts">
import HeartSvg from "@/assets/icons/heart.svg";
import HeartFillSvg from "@/assets/icons/heart.fill.svg";

defineProps<{
  state: boolean | undefined;
  no_emit?: boolean;
}>();

const emit = defineEmits<{
  (event: "handleFav"): void;
}>();
</script>

<style lang="scss">
$bg: rgb(250, 33, 33);

.heart-button {
  align-items: center;
  padding: 0 1rem;
  gap: $smaller;
  border: solid 1px $bg;
  background: transparent;
  color: rgb(250, 33, 33);

  &:hover {
    background: transparent;
  }
}
</style>
