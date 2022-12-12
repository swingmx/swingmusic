<template>
  <div class="artist-discography-nav">
    <h1 class="ellip">Creedence Clearwater Revival</h1>
    <div class="buttons">
      <!-- create dropdown -->
      <div class="select rounded-sm" v-auto-animate="{ duration: 100 }">
        <button class="selected" @click.prevent="showDropDown = !showDropDown">
          <span class="ellip">Albums and appearances</span>
          <ArrowSvg />
        </button>
        <div
          ref="dropOptionsRef"
          class="options rounded-sm"
          v-if="showDropDown"
        >
          <div class="option selected" value="1">Albums</div>
          <div class="option" value="2">Singles & EPs</div>
          <div class="option" value="3">Appearances</div>
        </div>
      </div>
      <button class="rounded-sm"><GridSvg /></button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onClickOutside } from "@vueuse/core";

import ArrowSvg from "@/assets/icons/expand.svg";
import GridSvg from "@/assets/icons/grid.svg";
import { Ref, ref } from "vue";

const showDropDown = ref(false);
const dropOptionsRef: Ref<HTMLElement | undefined> = ref();

function hideDropDown() {
  showDropDown.value = false;
}

onClickOutside(dropOptionsRef, (e) => {
  e.stopImmediatePropagation();
  hideDropDown();
});
</script>

<style lang="scss">
.artist-discography-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;

  h1 {
    margin: 0;
  }

  .buttons {
    display: flex;
    gap: $small;
  }

  .selected {
    display: grid;
    grid-template-columns: 1fr 2rem;
    gap: $smaller;
    width: 100%;
    padding-right: 0;

    svg {
      transform: rotate(90deg) scale(0.9);
    }
  }

  .select {
    position: relative;
    width: 7rem;
    display: flex;
    align-items: center;
    font-size: calc($medium + 2px);
    z-index: 10;

    .options {
      background-color: $gray;
      position: absolute;
      top: 120%;
      padding: $small $smaller;
      display: grid;
    }

    .option {
      padding: $small;
      border-bottom: 1px solid $gray4;
      width: 6.5rem;

      &:hover {
        border-radius: $smaller;
        border-bottom: 1px solid transparent;
        background-color: $darkestblue;
      }

      &:last-child {
        border-bottom: none;
      }
    }
  }
}
</style>
