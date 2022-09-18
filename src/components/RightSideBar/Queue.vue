<template>
  <QueueActions />
  <div
    class="scrollable-r"
    v-bind="containerProps"
    style="height: 100%"
    @mouseover="mouseover = true"
    @mouseout="mouseover = false"
  >
    <div class="inner" v-bind="wrapperProps">
      <TrackItem
        style="height: 64px"
        v-for="(t, index) in tracks"
        :key="t.index"
        :track="t.data"
        :index="index"
        :isPlaying="queue.playing"
        :isCurrent="t.index === queue.currentindex"
        :isQueueTrack="true"
        @PlayThis="playFromQueue(index)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import { useVirtualList } from "@vueuse/core";

// import { focusElem } from "@/utils";
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
  overscan: 10,
});

onMounted(() => {
  scrollTo(queue.currentindex);
});

// TODO: Handle focusing current track on song end
</script>

<style lang="scss">
.scrollable-r {
  height: 100%;
  overflow: auto;

  .inner {
    // scrollbar-color: grey transparent;
    margin-bottom: 1rem;
  }
}
</style>
