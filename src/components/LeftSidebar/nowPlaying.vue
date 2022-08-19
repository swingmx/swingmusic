<template>
  <div class="now-playing-card t-center rounded">
    <div>
      <SongCard :track="queue.currenttrack" />
      <div class="l-track-time">
        <span class="rounded">{{ formatSeconds(queue.duration.current) }}</span
        ><span class="rounded">{{ formatSeconds(queue.duration.full) }}</span>
      </div>
      <Progress />
    </div>
    <HotKeys />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import useModalStore from "@/stores/modal";
import useQueueStore from "@/stores/queue";
import useQStore from "../../stores/queue";
import useContextStore from "@/stores/context";
import MenuSvg from "../../assets/icons/more.svg";
import trackContext from "@/contexts/track_context";

import { ContextSrc } from "@/composables/enums";
import { formatSeconds } from "@/utils";

import HotKeys from "./NP/HotKeys.vue";
import Progress from "./NP/Progress.vue";
import SongCard from "./NP/SongCard.vue";

const queue = useQStore();
const contextStore = useContextStore();
const context_on = ref(false);

const showContextMenu = (e: Event) => {
  e.preventDefault();
  e.stopPropagation();

  const menus = trackContext(
    queue.tracklist[queue.current],
    useModalStore,
    useQueueStore
  );

  contextStore.showContextMenu(e, menus, ContextSrc.Track);
  context_on.value = true;

  contextStore.$subscribe((mutation, state) => {
    if (!state.visible) {
      context_on.value = false;
    }
  });
};
</script>
<style lang="scss">
.now-playing-card {
  padding: 1rem;
  width: 100%;
  display: grid;
  grid-template-rows: 1fr max-content;
  position: relative;
  gap: 1rem;

  .l-track-time {
    display: flex;
    justify-content: space-between;
    opacity: 0.8;
    margin-top: $small;

    span {
      font-size: small;
      padding: $smaller;
    }
  }

  &:hover {
    ::-moz-range-thumb {
      height: 0.8rem;
    }

    ::-webkit-slider-thumb {
      height: 0.8rem;
    }

    ::-ms-thumb {
      height: 0.8rem;
    }
  }


  .context_on {
    background-color: $accent;
  }

  .menu {
    right: $small;
    transform: rotate(90deg);
  }
}
</style>
