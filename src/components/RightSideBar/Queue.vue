<template>
  <QueueActions />
  <div
    ref="scrollable"
    id="queue-scrollable"
    v-bind="containerProps"
    style="height: 100%"
    @mouseover="mouseover = true"
    @mouseout="mouseover = false"
  >
    <div class="inner" v-bind="wrapperProps">
      <TrackItem
        style="height: 64px"
        v-for="t in tracks"
        :key="t.index"
        :track="t.data"
        :index="t.index"
        :isCurrentPlaying="t.index === queue.currentindex && queue.playing"
        :isCurrent="t.index === queue.currentindex"
        :isQueueTrack="true"
        @PlayThis="playFromQueue(t.index)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useVirtualList } from "@vueuse/core";
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

import useQStore from "@/stores/queue";

import TrackItem from "../shared/TrackItem.vue";
import QueueActions from "./Queue/QueueActions.vue";

const queue = useQStore();
const mouseover = ref(false);
const scrollable = ref<HTMLElement>();
const sourceTrackList = computed(() => queue.tracklist);
const {
  list: tracks,
  containerProps,
  wrapperProps,
} = useVirtualList(sourceTrackList, {
  itemHeight: 64,
});

function playFromQueue(index: number) {
  queue.play(index);
}

function scrollToCurrent() {
  const elem = document.getElementById("queue-scrollable") as HTMLElement;
  const itemHeight = 64;

  const top = queue.currentindex * itemHeight - itemHeight;
  elem.scroll({
    top,
    behavior: "smooth",
  });
}

onMounted(() => {
  queue.setScrollFunction(scrollToCurrent, mouseover);
});

onBeforeUnmount(() => {
  queue.setScrollFunction(() => {}, null);
});
</script>

<style lang="scss">
.scrollable-r {
  height: 100%;
  overflow: auto;

  .inner {
    margin-bottom: 1rem;
  }
}
</style>
