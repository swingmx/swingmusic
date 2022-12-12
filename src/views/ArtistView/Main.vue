<template>
  <div
    class="artist-page v-scroll-page"
    style="height: 100%"
    :class="{ isSmall, isMedium }"
  >
    <DynamicScroller
      :items="scrollerItems"
      :min-item-size="64"
      class="scroller"
      style="height: 100%"
    >
      <template v-slot="{ item, index, active }">
        <DynamicScrollerItem
          :item="item"
          :active="active"
          :size-dependencies="[item.props]"
          :data-index="index"
        >
          <component
            :key="index"
            :is="item.component"
            v-bind="item.props"
          ></component>
        </DynamicScrollerItem>
      </template>
    </DynamicScroller>
  </div>
</template>

<script setup lang="ts">
import { isMedium, isSmall } from "@/stores/content-width";

import Header from "@/components/ArtistView/Header.vue";
import TopTracks from "@/components/ArtistView/TopTracks.vue";
import useArtistPageStore from "@/stores/pages/artist";
import ArtistAlbums from "@/components/AlbumView/ArtistAlbums.vue";
import ArtistAlbumsFetcher from "@/components/ArtistView/ArtistAlbumsFetcher.vue";
import { computed } from "vue";
import { onBeforeRouteLeave, onBeforeRouteUpdate, useRoute } from "vue-router";
import { Album } from "@/interfaces";
import { discographyAlbumTypes } from "@/composables/enums";

const store = useArtistPageStore();
const route = useRoute();

interface ScrollerItem {
  id: string | number;
  component: any;
  props?: Record<string, unknown>;
}

const header: ScrollerItem = {
  id: "artist-header",
  component: Header,
};

const top_tracks: ScrollerItem = {
  id: "artist-top-tracks",
  component: TopTracks,
};

const artist_albums_fetcher: ScrollerItem = {
  id: "artist-albums-fetcher",
  component: ArtistAlbumsFetcher,
};

enum AlbumType {
  ALBUMS = "Albums",
  EPS = "EPs",
  SINGLES = "Singles",
  APPEARANCES = "Appearances",
}

function createAbumComponent(title: AlbumType, albums: Album[]) {
  let albumType = null;

  switch (title) {
    case AlbumType.ALBUMS:
      albumType = discographyAlbumTypes.albums;
      break;
    case AlbumType.EPS:
      albumType = discographyAlbumTypes.eps;
      break;
    case AlbumType.SINGLES:
      albumType = discographyAlbumTypes.singles;
      break;
    case AlbumType.APPEARANCES:
      albumType = discographyAlbumTypes.appearances;
      break;

    default:
      break;
  }
  return {
    id: title,
    component: ArtistAlbums,
    props: {
      albumType,
      albums,
      title,
      artisthash: route.params.hash,
    },
  };
}

const scrollerItems = computed(() => {
  let components = [header];

  if (store.tracks.length > 0) {
    components.push(top_tracks);
  }

  components = [...components, artist_albums_fetcher];

  if (store.albums.length > 0) {
    const albums = createAbumComponent(AlbumType.ALBUMS, store.albums);
    components.push(albums);
  }

  if (store.eps.length > 0) {
    const eps = createAbumComponent(AlbumType.EPS, store.eps);
    components.push(eps);
  }

  if (store.singles.length > 0) {
    const singles = createAbumComponent(AlbumType.SINGLES, store.singles);
    components.push(singles);
  }

  if (store.appearances.length > 0) {
    const appearances = createAbumComponent(
      AlbumType.APPEARANCES,
      store.appearances
    );
    components.push(appearances);
  }

  return components;
});

onBeforeRouteUpdate(async (to) => {
  await store.getData(to.params.hash as string);
});

onBeforeRouteLeave(async () => {
  setTimeout(() => {
    store.resetAlbums();
  }, 400);
});
</script>

<style lang="scss">
.artist-page {
  .artist-albums {
    margin-top: 2rem;
  }

  .section-title {
    margin: 1rem;
    padding-left: 1rem;
  }
}
</style>
