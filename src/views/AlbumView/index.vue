<template>
  <div class="album-virtual-scroller v-scroll-page">
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
        @playThis="playFromAlbum(item.props.index - item.props.track.disc - 1)"
      />
    </RecycleScroller>
  </div>
</template>

<script setup lang="ts">
import {
  onBeforeRouteLeave,
  onBeforeRouteUpdate,
  RouteLocationNormalized,
} from "vue-router";
import { computed } from "@vue/reactivity";

import { Track } from "@/interfaces";
import { createTrackProps } from "@/utils";

import useQueueStore from "@/stores/queue";
import useAlbumStore from "@/stores/pages/album";

import Header from "@/components/AlbumView/Header.vue";
import SongItem from "@/components/shared/SongItem.vue";
import AlbumDiscBar from "@/components/AlbumView/AlbumDiscBar.vue";

const album = useAlbumStore();
const queue = useQueueStore();

interface ScrollerItem {
  id: string;
  component: typeof Header | typeof SongItem;
  props: Record<string, unknown>;
  size: number;
}

class songItem {
  id: number;
  props = {};
  size = 64;
  component: typeof SongItem | typeof AlbumDiscBar;

  constructor(track: Track) {
    this.id = Math.random();
    this.props = track.is_album_disc_number
      ? { album_disc: track }
      : createTrackProps(track);
    this.component = track.is_album_disc_number ? AlbumDiscBar : SongItem;
  }
}

function getSongItems() {
  return album.tracks.map((track) => {
    return new songItem(track);
  });
}

const scrollerItems = computed(() => {
  const header: ScrollerItem = {
    id: "album-header",
    component: Header,
    props: {
      album: album.info,
    },
    size: 18 * 16,
  };

  return [header, ...getSongItems()];
});

function playFromAlbum(index: number) {
  const { title, artist, hash } = album.info;
  queue.playFromAlbum(title, artist, hash, album.allTracks);
  queue.play(index);
}

onBeforeRouteUpdate(async (to: RouteLocationNormalized) => {
  await album
    .fetchTracksAndArtists(to.params.hash.toString())
    .then(() => album.resetQuery());
});

onBeforeRouteLeave(() => {
  setTimeout(() => {
    album.resetQuery();
  }, 500);
});
</script>

<style lang="scss">
.album-virtual-scroller {
  height: 100%;
  .scroller {
    padding-bottom: $content-padding-bottom;
  }
}
</style>
