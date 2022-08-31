<template>
  <div class="up-next">
    <div class="r-grid">
      <div class="scrollable-r rounded">
        <QueueActions />
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
.up-next {
  overflow: hidden;
  height: 100%;

  .heading {
    position: relative;
    margin: 0.5rem 0 1rem 0;
  }

  .r-grid {
    position: relative;
    height: 100%;

    .scrollable-r {
      height: 100%;
      overflow: hidden;
      display: grid;
      grid-template-rows: max-content 1fr;

      .inner {
        overflow: scroll;
        overflow-x: hidden;
        scrollbar-color: grey transparent;
        margin: 1rem 0;
      }
    }
  }
}
</style>
