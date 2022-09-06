<template>
  <div id="back-forward" class="">
    <button class="back" @click="$router.back()">
      <ArrowSvg />
    </button>
    <button class="forward" @click="$router.forward()">
      <ArrowSvg />
    </button>
  </div>
</template>

<script setup lang="ts">
import ArrowSvg from "../../assets/icons/right-arrow.svg";
</script>

<style lang="scss">
#back-forward {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  padding-right: 1rem;
  border-right: 1px solid $gray3;
  height: 100%;

  & > * {
    width: 2.25rem;
    aspect-ratio: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0;
    border-radius: 0.65rem;

    svg {
      transform: scale(1.25);
      transition: all .2s;

      &:active {
        transform: scale(1);
      }
    }
  }

  .back {
    transform: rotate(180deg);
  }
}
</style>
