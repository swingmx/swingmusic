<template>
  <div
    class="queue-view-virtual-scroller v-scroll-page"
    :class="{ isSmall, isMedium }"
    style="height: 100%"
  >
    <RecycleScroller
      class="scroller"
      id="queue-page-scrollable"
      style="height: 100%"
      :items="scrollerItems"
      :item-size="itemHeight"
      key-field="id"
      v-slot="{ item, index }"
    >
      <SongItem
        :track="item.track"
        :index="index + 1"
        :isCurrent="queue.currenttrackhash === item.track.trackhash"
        :isCurrentPlaying="
          queue.currenttrackhash === item.track.trackhash && queue.playing
        "
        @playThis="playFromQueue(index)"
      />
    </RecycleScroller>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";

import SongItem from "@/components/shared/SongItem.vue";
import { isMedium, isSmall } from "@/stores/content-width";
import useQStore from "@/stores/queue";
import { createTrackProps } from "@/utils";

const itemHeight = 64;
const queue = useQStore();

const scrollerItems = computed(() => {
  return queue.tracklist.map((track) => {
    return {
      track,
      id: Math.random(),
      props: createTrackProps(track),
    };
  });
});

function playFromQueue(index: number) {
  queue.play(index);
}

function scrollToCurrent() {
  const scrollable = document.getElementById("queue-page-scrollable");
  const itemHeight = 64;
  const top = (queue.currentindex - 1) * itemHeight;

  scrollable?.scrollTo({
    top,
    behavior: "smooth",
  });
}

onMounted(() => {
  setTimeout(() => {
    scrollToCurrent();
  }, 1000);
});
</script>

<style lang="scss">
.queue-view-virtual-scroller {
  .songlist-item.current {
    background-color: $darkestblue !important;
  }
}
</style>
