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
          @playThis="playFromAlbum(item.props.track.master_index)"
        />
      </div>
    </RecycleScroller>
  </div>
</template>

<script setup lang="ts">
import { computed } from "@vue/reactivity";
import { onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";

import { Track } from "@/interfaces";

import useAlbumStore from "@/stores/pages/album";
import useQueueStore from "@/stores/queue";

import AlbumDiscBar from "@/components/AlbumView/AlbumDiscBar.vue";
import ArtistAlbums from "@/components/AlbumView/ArtistAlbums.vue";
import GenreBanner from "@/components/AlbumView/GenreBanner.vue";
import Header from "@/components/AlbumView/Header.vue";
import SongItem from "@/components/shared/SongItem.vue";

import { isSmall } from "@/stores/content-width";
import { discographyAlbumTypes } from "@/composables/enums";

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
      : { track, hide_album: true, index: track.track };
    this.component = track.is_album_disc_number ? AlbumDiscBar : SongItem;
  }
}

const genreBanner: ScrollerItem = {
  id: "genre-banner",
  component: GenreBanner,
  size: 80,
};

function getSongItems() {
  return album.tracks.map((track) => {
    return new songItem(track);
  });
}

function getArtistAlbumComponents(): ScrollerItem[] {
  return album.albumArtists.map((ar) => {
    const artist = album.info.albumartists.find(
      (a) => a.artisthash === ar.artisthash
    );
    const artistname = artist?.name;
    const artisthash = artist?.artisthash;

    return {
      id: Math.random().toString(),
      component: ArtistAlbums,
      props: {
        artisthash,
        albums: ar.albums,
        title: `More from ${artistname}`,
        albumType: discographyAlbumTypes.all,
        route: `/artists/${artisthash}/discography`,
      },
      size: 20 * 16,
    };
  });
}

const scrollerItems = computed(() => {
  const header: ScrollerItem = {
    id: "album-header",
    component: Header,
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
  const { title, albumhash } = album.info;
  queue.playFromAlbum(title, albumhash, album.srcTracks);
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
    grid-template-columns: 1.75rem 1.5fr 1fr 2.5rem 2.5rem;
  }
}
</style>
