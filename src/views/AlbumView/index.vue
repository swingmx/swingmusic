<template>
  <div class="album-virtual-scroller v-scroll-page" :class="{ isSmall }">
    <RecycleScroller
      class="scroller"
      :items="scrollerItems"
      :item-size="null"
      key-field="id"
      v-slot="{ item }"
    >
      <div :style="{ maxHeight: `${item.size}px` }">
        <component
          :is="item.component"
          v-bind="item.props"
          @playThis="
            playFromAlbum(item.props.track.index - item.props.track.disc)
          "
        />
      </div>
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
    const artist_name = album.info.albumartists.find(
      (a) => a.artisthash === artist.artisthash
    )?.name;
    return {
      id: Math.random().toString(),
      component: ArtistAlbums,
      props: { title: `More from ${artist_name}`, albums: artist.albums },
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
  const { title, albumartists, albumhash } = album.info;
  queue.playFromAlbum(title, albumhash, album.allTracks);
  queue.play(index);
}

onBeforeRouteUpdate(async (to) => {
  await album.fetchTracksAndArtists(to.params.hash.toString()).then(() => {
    album.resetQuery();
    album.resetAlbumArtists();
    album.fetchArtistAlbums();
  });
});

onBeforeRouteLeave(() => {
  setTimeout(() => {
    album.resetQuery();
    album.resetAlbumArtists();
  }, 500);
});
</script>

<style lang="scss">
.album-virtual-scroller {
  height: 100%;
  overflow: visible;
  .songlist-item {
    grid-template-columns: 1.5rem 1.5fr 1fr 2.5rem 2.5rem;
  }
}
</style>
