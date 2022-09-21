<template>
  <div class="header-list-layout">
    <div
      v-bind="containerProps"
      style="height: calc(100vh - 4.25rem)"
      :style="{ paddingTop: !no_header ? headerHeight - 64 + 16 + 'px' : 0 }"
      @scroll="handleScroll"
    >
      <div v-bind="wrapperProps" class="scrollable">
        <div class="header rounded" style="height: 64px" v-if="!no_header">
          <div
            ref="header"
            :style="{ top: -headerHeight + 64 - 16 + 'px' }"
            class="header-content"
          >
            <slot name="header"></slot>
          </div>
        </div>
        <SongItem
          style="height: 60px"
          v-for="t in tracks"
          :key="t.data.trackid"
          :track="t.data"
          :index="
            on_album_page
              ? t.data.track
              : t.data.index !== undefined
              ? t.data.index + 1
              : t.index + 1
          "
          :isPlaying="queue.playing"
          :isCurrent="queue.currentid == t.data.trackid"
          @playThis="
            updateQueue(t.data.index !== undefined ? t.data.index : t.index)
          "
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { useElementSize, useVirtualList } from "@vueuse/core";

import { Track } from "@/interfaces";
import useQStore from "@/stores/queue";

import SongItem from "@/components/shared/SongItem.vue";

const props = defineProps<{
  tracks: Track[];
  on_album_page?: boolean;
  no_header?: boolean;
}>();

const emit = defineEmits<{
  (e: "playFromPage", index: number): void;
}>();

const queue = useQStore();
const header = ref<HTMLElement>();
const source = computed(() => props.tracks);
const { height: headerHeight } = useElementSize(header);

const {
  list: tracks,
  containerProps,
  wrapperProps,
} = useVirtualList(source, {
  itemHeight: 60,
  overscan: 15,
});

function updateQueue(index: number) {
  emit("playFromPage", index);
}

function handleScroll(e: Event) {
  const scrollTop = (e.target as HTMLElement).scrollTop;

  if (scrollTop > headerHeight.value) {
    header.value ? (header.value.style.opacity = "0") : null;
  } else {
    header.value ? (header.value.style.opacity = "1") : null;
  }
}
</script>

<style lang="scss">
.header-list-layout {
  margin-right: calc(0rem - ($medium));

  .scrollable {
    padding-right: calc(1rem - $small + 2px);
    scrollbar-width: thin;
  }

  .header {
    position: relative;

    .header-content {
      position: absolute;
      width: 100%;
    }
  }
}
</style>
