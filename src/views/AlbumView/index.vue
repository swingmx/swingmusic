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
        :style="{ maxHeight: `${item.size}px` }"
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
  RouteLocationNormalized,
} from "vue-router";

import { Track } from "@/interfaces";
import { createTrackProps } from "@/utils";

import useAlbumStore from "@/stores/pages/album";
import useQueueStore from "@/stores/queue";

import AlbumDiscBar from "@/components/AlbumView/AlbumDiscBar.vue";
import ArtistAlbums from "@/components/AlbumView/ArtistAlbums.vue";
import GenreBanner from "@/components/AlbumView/GenreBanner.vue";
import Header from "@/components/AlbumView/Header.vue";
import SongItem from "@/components/shared/SongItem.vue";

import { isSmall } from "@/stores/content-width";

const album = useAlbumStore();
const queue = useQueueStore();

interface ScrollerItem {
  id: string;
  component:
    | typeof Header
    | typeof SongItem
    | typeof GenreBanner
    | typeof ArtistAlbums;
  props?: any;
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

const genreBanner: ScrollerItem = {
  id: "genre-banner",
  component: GenreBanner,
  size: 64,
};

function getSongItems() {
  return album.tracks.map((track) => {
    return new songItem(track);
  });
}

function getArtistAlbumComponents(): ScrollerItem[] {
  return album.albumArtists.map((artist) => {
    return {
      id: Math.random().toString(),
      component: ArtistAlbums,
      props: { artist },
      size: 20 * 16,
    };
  });
}

const scrollerItems = computed(() => {
  const header: ScrollerItem = {
    id: "album-header",
    component: Header,
    props: {
      album: album.info,
    },
    size: 19 * 16,
  };

  return [
    header,
    ...getSongItems(),
    genreBanner,
    ...getArtistAlbumComponents(),
  ];
});

function playFromAlbum(index: number) {
  const { title, albumartist, albumhash } = album.info;
  queue.playFromAlbum(title, albumartist, albumhash, album.allTracks);
  queue.play(index);
}

onBeforeRouteUpdate(async (to: RouteLocationNormalized) => {
  await album.fetchTracksAndArtists(to.params.hash.toString()).then(() => {
    album.resetQuery();
    album.resetAlbumArtists();
    album.fetchArtistAlbums();
  });
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

  .songlist-item {
    grid-template-columns: 1.5rem 1.5fr 1fr 2.5rem 2.5rem;
  }
}
</style>
