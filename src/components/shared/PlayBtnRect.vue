<template>
  <div
    class="playbtnrect rounded"
    @click="usePlayFrom(source, useQStore, store)"
  >
    <div class="icon image"></div>
    <div class="text">Play</div>
  </div>
</template>

<script setup lang="ts">
import { playSources } from "@/composables/enums";
import usePlayFrom from "@/composables/usePlayFrom";
import useQStore from "@/stores/queue";
import useFStore from "@/stores/folder";
import useAStore from "@/stores/album";
import usePStore from "@/stores/p.ptracks";

defineProps<{
  source: playSources;
  store:
    | typeof useQStore
    | typeof useFStore
    | typeof useAStore
    | typeof usePStore;
}>();
</script>

<style lang="scss">
.playbtnrect {
  width: 6rem;
  display: flex;
  align-items: center;
  height: 2.5rem;
  padding-left: 0.75rem;
  cursor: pointer;
  background: linear-gradient(34deg, $accent, $red);
  user-select: none;
  transition: all 0.5s ease-in-out;

  .icon {
    height: 2rem;
    width: 2rem;
    background-image: url("../../assets/icons/play.svg");
  }

  &:hover {
    .icon {
      transform: rotate(120deg);
    }
  }
}
</style>
