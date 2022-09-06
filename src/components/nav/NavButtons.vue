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
  width: max-content;
  height: 100%;

  & > * {
    width: 2.25rem;
    background-color: $gray3;
    aspect-ratio: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0;
  }

  .back {
    transform: rotate(180deg);
  }
}
</style>
