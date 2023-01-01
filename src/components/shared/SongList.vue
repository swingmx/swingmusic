<template>
  <div
    class="queue-view-virtual-scroller v-scroll-page"
    :class="{ isSmall, isMedium }"
    style="height: 100%"
  >
    <RecycleScroller
      class="scroller"
      id="songlist-scroller"
      style="height: 100%"
      :items="tracks.map((track) => ({ track, id: Math.random() }))"
      :item-size="itemHeight"
      key-field="id"
      v-slot="{ item, index }"
    >
      <SongItem
        :track="item.track"
        :index="index + 1"
        @playThis="handlePlay(index)"
      />
    </RecycleScroller>
  </div>
</template>

<script setup lang="ts">
import SongItem from "@/components/shared/SongItem.vue";
import { isMedium, isSmall } from "@/stores/content-width";
import { Track } from "@/interfaces";

defineProps<{
  tracks: Track[];
  handlePlay: (index: number) => void;
}>();

const itemHeight = 64;
</script>