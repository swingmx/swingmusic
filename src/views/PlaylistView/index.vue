<template>
  <div
    class="playlist-virtual-scroller v-scroll-page"
    :class="{ isSmall, isMedium }"
    style="height: 100%"
  >
    <RecycleScroller
      class="scroller"
      :items="scrollerItems"
      :item-size="null"
      key-field="id"
      v-slot="{ item }"
      style="height: 100%"
    >
      <component
        :is="item.component"
        v-bind="item.props"
        @playThis="playFromPlaylistPage(item.props.index - 1)"
      />
    </RecycleScroller>
  </div>
</template>

<script setup lang="ts">
import { computed } from "@vue/reactivity";
import { onBeforeRouteLeave } from "vue-router";

import { isMedium, isSmall } from "@/stores/content-width";
import usePlaylistStore from "@/stores/pages/playlist";
import useQueueStore from "@/stores/queue";

import Header from "@/components/PlaylistView/Header.vue";
import SongItem from "@/components/shared/SongItem.vue";

const queue = useQueueStore();
const playlist = usePlaylistStore();

interface ScrollerItem {
  id: string | number;
  component: typeof Header | typeof SongItem;
  // props: Record<string, unknown>;
  size: number;
}

const header: ScrollerItem = {
  id: "header",
  component: Header,
  size: 19 * 16,
};

const scrollerItems = computed(() => {
  return [
    header,
    ...playlist.tracks.map((track) => {
      return {
        id: Math.random(),
        component: SongItem,
        props: {
          track: track,
          index: track.index + 1,
          isCurrent: queue.currentid === track.id,
          isCurrentPlaying: queue.currentid === track.id && queue.playing,
        },
        size: 64,
      };
    }),
  ];
});

function playFromPlaylistPage(index: number) {
  const { name, id } = playlist.info;
  queue.playFromPlaylist(name, id, playlist.allTracks);
  queue.play(index);
}

onBeforeRouteLeave(() => {
  setTimeout(() => {
    playlist.resetQuery();
  }, 500);
});
</script>
