<template>
    <QueueActions />
    <div class="scrollable-r">
      <div class="inner">
        <TrackComponent
          v-for="(t, index) in queue.tracklist"
          :key="index"
          :track="t"
          :index="index + 1"
          :isPlaying="queue.playing"
          :isHighlighted="false"
          :isCurrent="index === queue.currentindex"
        />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onUpdated, ref } from "vue";

import useQStore from "@/stores/queue";
import { focusElem } from "@/utils";

import TrackItem from "../shared/TrackItem.vue";
import SongItem from "../shared/SongItem.vue";
import QueueActions from "./Queue/QueueActions.vue";

const props = defineProps<{
  isOnQueuePage?: boolean;
}>();

const TrackComponent = computed(() => {
  if (props.isOnQueuePage) {
    return SongItem;
  }

  return TrackItem;
});

const queue = useQStore();
const mouseover = ref(false);

function setMouseOver(val: boolean) {
  mouseover.value = val;
}

onUpdated(() => {
  if (mouseover.value) return;

  setTimeout(() => {
    focusElem("currentInQueue");
  }, 1000);
});
</script>

<style lang="scss">
.scrollable-r {
  height: 100%;
  overflow: auto;

  .inner {
    scrollbar-color: grey transparent;
    margin: 1rem 0;
  }
}
</style>
