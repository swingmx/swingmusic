<template>
  <QueueActions />
  <div
    class="scrollable-r"
    v-bind="containerProps"
    style="height: 100%"
    @mouseover="mouseover = true"
    @mouseout="mouseover = false"
  >
    <div class="inner" v-bind="wrapperProps" >
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

function playFromQueue(index: number) {
  queue.play(index);
}

const source = computed(() => queue.tracklist);

const {
  list: tracks,
  containerProps,
  wrapperProps,
  scrollTo,
} = useVirtualList(source, {
  itemHeight: 64,
});

onMounted(() => {
  scrollTo(queue.currentindex);
  queue.setScrollFunction(scrollTo, mouseover);
});

onBeforeUnmount(() => {
  queue.setScrollFunction(() => {}, null);
});

// TODO: Handle focusing current track on song end
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
