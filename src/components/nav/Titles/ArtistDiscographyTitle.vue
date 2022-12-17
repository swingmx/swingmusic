<template>
  <div class="artist-discography-nav">
    <h1 class="ellip">{{ store.artistname }}</h1>
    <div class="buttons">
      <div class="select rounded-sm" v-auto-animate="{ duration: 10 }">
        <button class="selected" @click.prevent="showDropDown = !showDropDown">
          <span class="ellip">{{ store.page }}</span>
          <ArrowSvg />
        </button>
        <div
          ref="dropOptionsRef"
          class="options rounded-sm shadow-lg"
          v-if="showDropDown"
        >
          <div
            class="option"
            v-for="a in albums"
            @click.prevent="switchView(a)"
          >
            {{ a }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onClickOutside } from "@vueuse/core";

import ArrowSvg from "@/assets/icons/expand.svg";
import GridSvg from "@/assets/icons/grid.svg";
import { Ref, ref } from "vue";
import { discographyAlbumTypes as albums } from "@/composables/enums";

import useArtistDiscogStore from "@/stores/pages/artistDiscog";

const store = useArtistDiscogStore();

const showDropDown = ref(false);
const dropOptionsRef: Ref<HTMLElement | undefined> = ref();

function hideDropDown() {
  showDropDown.value = false;
}

function switchView(album: albums) {
  store.setAlbums(album);
  hideDropDown();
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
    width: 8rem;
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
      width: 7.5rem;

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
