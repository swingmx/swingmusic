<template>
  <!-- JUST A COMMENT: 64 is single item height, 24 is gap height -->
  <div class="header-list-layout">
    <div
      id="v-page-scrollable"
      v-bind="containerProps"
      style="height: 100%"
      @scroll="handleScroll"
    >
      <div
        v-bind="wrapperProps"
        class="v-list"
        ref="v_list"
        :class="{
          isSmall: isSmall,
          isMedium: isMedium || on_album_page,
        }"
      >
        <div
          ref="header"
          class="header rounded"
          v-if="!no_header"
          :style="{ height: headerHeight + (on_album_page ? 0 : 24) + 'px' }"
        >
          <div ref="header_content" class="header-content">
            <slot name="header"></slot>
          </div>
        </div>
        <div v-for="t in tracks">
          <AlbumDiscBar
            v-if="on_album_page && t.data.is_album_disc_number"
            :album_disc="t.data"
          />

          <SongItem
            v-else
            style="height: 60px"
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
        </div>
        <div class="page-bottom-padding" style="height: 64px"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useElementSize, useVirtualList } from "@vueuse/core";
import { computed, onMounted, onUpdated, ref, watch } from "vue";

import { Track } from "@/interfaces";
import useQStore from "@/stores/queue";

import SongItem from "@/components/shared/SongItem.vue";
import AlbumDiscBar from "@/components/AlbumView/AlbumDiscBar.vue";
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
let scrollable: HTMLElement;
const v_list = ref<HTMLElement>();
const header_content = ref<HTMLElement>();
const { width } = useElementSize(v_list);

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
  overscan: 20,
});

// watch source changes and scroll to top
watch(source, () => {
  scrollable.scroll(0, 0);
});

// HEADER
const header = ref<HTMLElement>();
const { height: headerHeight } = useElementSize(header_content);

function handleScroll(e: Event) {
  const scrollTop = (e.target as HTMLElement).scrollTop;

  if (scrollTop > (header.value?.offsetHeight || 0)) {
    header.value ? (header.value.style.opacity = "0") : null;
  } else {
    header.value ? (header.value.style.opacity = "1") : null;
  }
}

onMounted(() => {
  scrollable = document.getElementById("v-page-scrollable") as HTMLElement;
});
</script>

<style lang="scss">
.header-list-layout {
  margin-right: -$medium;
  height: 100%;

  .v-list {
    padding-right: calc(1rem - $small + 2px);
    scrollbar-width: thin;

    .current {
      background-color: $gray5;

      a {
        color: inherit;
      }
    }
  }

  .v-list.isSmall {
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

  .v-list.isMedium {
    // hide album column
    .songlist-item {
      grid-template-columns: 1.5rem 1.5fr 1fr 2.5rem 2.5rem;
    }

    .song-album {
      display: none !important;
    }
  }
}
</style>
