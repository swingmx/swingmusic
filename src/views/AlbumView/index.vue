<template>
  <div class="album-virtual-scroller v-scroll-page" :class="{ isSmall }">
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
        @playThis="
          playFromAlbum(item.props.track.index - item.props.track.disc)
        "
      />
    </RecycleScroller>
  </div>
</template>

<script setup lang="ts">
import { computed } from "@vue/reactivity";
import {
onBeforeRouteLeave,
onBeforeRouteUpdate,
RouteLocationNormalized
} from "vue-router";

import { Track } from "@/interfaces";
import { createTrackProps } from "@/utils";

import useAlbumStore from "@/stores/pages/album";
import useQueueStore from "@/stores/queue";

import AlbumDiscBar from "@/components/AlbumView/AlbumDiscBar.vue";
import Header from "@/components/AlbumView/Header.vue";
import SongItem from "@/components/shared/SongItem.vue";
import { isSmall } from "@/stores/content-width";

const album = useAlbumStore();
const queue = useQueueStore();

interface ScrollerItem {
  id: string;
  component: typeof Header | typeof SongItem;
  props: any;
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
      : { ...createTrackProps(track), hide_album: true, index: track.track };
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

  .songlist-item {
    grid-template-columns: 1.5rem 1.5fr 1fr 2.5rem 2.5rem;
  }
}
</style>
