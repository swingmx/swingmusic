<template>
  <div
    class="next-track bg-primary rounded"
    :class="{ contexton: context_on }"
    @click="playNext"
    @contextmenu.prevent="showMenu"
  >
    <div class="nextup abs">next up</div>
    <img :src="paths.images.thumb + track?.image" class="rounded-sm" />
    <div class="tags">
      <div class="title ellip">{{ track?.title || "Don't click here" }}</div>
      <div class="artist ellip" v-if="track">
        <span v-for="artist in putCommas(track.artists)" :key="artist">{{
          artist
        }}</span>
      </div>
      <span v-else class="artist">nothing will happen</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { paths } from "@/config";
import { Track } from "@/interfaces";
import { putCommas } from "@/utils";

import { showTrackContextMenu as showContext } from "@/composables/context";
import { ref } from "vue";

const props = defineProps<{
  track: Track | null;
  playNext: () => void;
}>();

const context_on = ref(false);

function showMenu(e: Event) {
  if (props.track) {
    showContext(e, props.track, context_on);
  }
}
</script>

<style lang="scss">
.next-track {
  position: relative;

  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 1rem;
  padding: 1rem;
  width: 100%;

  &:hover {
    background-color: $gray4;

    .h {
      background-color: $black;
    }
  }

  .nextup {
    right: $small;
    top: 0;
    font-size: 0.8rem;
    padding: $smaller;
    border-radius: 0.25rem;
    font-style: oblique;
    opacity: 0.5;
  }

  img {
    width: 4.5rem;
    aspect-ratio: 1;
    object-fit: contain;
  }

  .tags {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    gap: $small;

    .artist {
      font-size: small;
    }
  }
}
</style>
