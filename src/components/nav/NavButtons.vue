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
  padding-right: 1.25rem;
  border-right: 1px solid $gray3;
  width: 100%;

  & > * {
    background-color: $gray3;
    padding: $small;
    height: 100%;
    aspect-ratio: 1;
    border-radius: $medium;

    svg {
      margin: auto;
    }
  }

  .back {
    transform: rotate(180deg);
  }
}
</style>
