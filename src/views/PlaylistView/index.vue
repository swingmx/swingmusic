<template>
  <div class="playlist-virtual-scroller v-scroll-page">
    <RecycleScroller
      class="scroller"
      :items="scrollerItems"
      :item-size="null"
      key-field="id"
      v-slot="{ item }"
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

import useQueueStore from "@/stores/queue";
import usePlaylistStore from "@/stores/pages/playlist";

import Header from "@/components/PlaylistView/Header.vue";
import SongItem from "@/components/shared/SongItem.vue";

const queue = useQueueStore();
const playlist = usePlaylistStore();

interface ScrollerItem {
  id: string;
  component: typeof Header | typeof SongItem;
  props: Record<string, unknown>;
  size: number;
}

const header: ScrollerItem = {
  id: "header",
  component: Header,
  props: {
    info: playlist.info,
  },
  size: 19 * 16,
};

const scrollerItems = computed(() => {
  return [
    header,
    ...playlist.tracks.map((track) => {
      return {
        id: track.trackid,
        component: SongItem,
        props: {
          track: track,
          index: track.index + 1,
          isCurrent: queue.currentid === track.trackid,
          isCurrentPlaying: queue.currentid === track.trackid && queue.playing,
        },
        size: 64,
      };
    }),
  ];
});

function playFromPlaylistPage(index: number) {
  const { name, playlistid } = playlist.info;
  queue.playFromPlaylist(name, playlistid, playlist.allTracks);
  queue.play(index);
}

onBeforeRouteLeave(() => {
  setTimeout(() => {
    playlist.resetQuery();
  }, 500);
});
</script>

<style lang="scss">
.playlist-virtual-scroller {
  height: 100%;
  width: 100%;
  
  .scroller {
    height: 100%;
    width: 100%;
    padding-bottom: 4rem;
  }
}
</style>
