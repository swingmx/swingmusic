<template>
  <!-- JUST A COMMENT: 64 is single item height, 24 is gap height -->
  <div class="header-list-layout">
    <div
      v-bind="containerProps"
      style="height: 100%"
      :style="{ paddingTop: !no_header ? headerHeight - 64 + 24 + 'px' : 0 }"
      @scroll="handleScroll"
    >
      <div
        v-bind="wrapperProps"
        class="scrollable"
        ref="scrollable"
        :class="{
          isSmall: isSmall,
          isMedium: isMedium || on_album_page,
        }"
      >
        <div class="header rounded" style="height: 64px" v-if="!no_header">
          <div
            ref="header"
            :style="{ top: -headerHeight + 64 - 24 + 'px' }"
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
          :no_album="on_album_page"
          :index="
            on_album_page
              ? t.data.track
              : t.data.index !== undefined
              ? t.data.index + 1
              : t.index + 1
          "
          :isCurrent="queue.currentid === t.data.trackid"
          :isCurrentPlaying="
            queue.currentid === t.data.trackid && queue.playing
          "
          @playThis="
            updateQueue(t.data.index !== undefined ? t.data.index : t.index)
          "
        />
        <div class="page-bottom-padding" style="height: 64px"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useElementSize, useVirtualList } from "@vueuse/core";
import { computed, ref } from "vue";

import { Track } from "@/interfaces";
import useQStore from "@/stores/queue";

import SongItem from "@/components/shared/SongItem.vue";

// EMITS & PROPS
const emit = defineEmits<{
  (e: "playFromPage", index: number): void;
}>();

const props = defineProps<{
  tracks: Track[];
  on_album_page?: boolean;
  no_header?: boolean;
}>();

// QUEUE
const queue = useQStore();
function updateQueue(index: number) {
  emit("playFromPage", index);
}

// SCROLLABLE AREA
const scrollable = ref<HTMLElement>();
const { width } = useElementSize(scrollable);

const brk = {
  sm: 500,
  md: 800,
};

const isSmall = computed(() => width.value < brk.sm);
const isMedium = computed(() => width.value > brk.sm && width.value < brk.md);

// VIRTUAL LIST
const source = computed(() => props.tracks);
const {
  list: tracks,
  containerProps,
  wrapperProps,
} = useVirtualList(source, {
  itemHeight: 60,
  overscan: 15,
});

// HEADER
const header = ref<HTMLElement>();
const { height: headerHeight } = useElementSize(header);

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
  margin-right: -$medium;
  height: 100%;

  .scrollable {
    padding-right: calc(1rem - $small + 2px);
    scrollbar-width: thin;

    .current {
      background-color: $gray5;

      a {
        color: inherit;
      }
    }
  }

  .scrollable.isSmall {
    // hide album and artists columns
    .songlist-item {
      grid-template-columns: 1.5rem 2fr 2.5rem 2.5rem;
    }

    .song-artists,
    .song-album {
      display: none !important;
    }

    .isSmallArtists {
      display: unset !important;
      font-size: small;
      color: $white;
      opacity: 0.67;
    }
  }

  .scrollable.isMedium {
    // hide album column
    .songlist-item {
      grid-template-columns: 1.5rem 1.5fr 1fr 2.5rem 2.5rem;
    }

    .song-album {
      display: none !important;
    }
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
