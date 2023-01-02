<template>
  <div class="search-tracks-view">
    <div
      :class="{ isSmall, isMedium }"
      style="height: 100%"
    >
      <RecycleScroller
        id="songlist-scroller"
        style="height: 100%"
        :items="search.tracks.value.map((track) => ({ track, id: Math.random() }))"
        :item-size="64"
        key-field="id"
        v-slot="{ item, index }"
      >
        <SongItem
          :track="item.track"
          :index="index + 1"
          @playThis="playFromSearch(index)"
        />
      </RecycleScroller>
    </div>
  </div>
</template>

<script setup lang="ts">
import useQueueStore from "@/stores/queue";
import useSearchStore from "@/stores/search";
import { isMedium, isSmall } from "@/stores/content-width";
import SongItem from "@/components/shared/SongItem.vue";

const search = useSearchStore();
const queue = useQueueStore();

function playFromSearch(index: number) {
  queue.playFromSearch(search.query, search.tracks.value);
  queue.play(index);
}
</script>

<style lang="scss">
.search-tracks-view {
  height: 100%;

  .no-scroll {
    height: 100%;
  }

  #songlist-scroller{
    padding-right: 1rem;
    padding-left: 0;
  }
}
</style>
