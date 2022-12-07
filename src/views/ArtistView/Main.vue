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
          <!-- @playThis="playFromPage(item.props.index - 1)" -->
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
import { onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";
import { Album } from "@/interfaces";

const store = useArtistPageStore();

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

function createAbumComponent(title: string, albums: Album[]) {
  return {
    id: title,
    component: ArtistAlbums,
    props: {
      title,
      albums,
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
    const albums = createAbumComponent("Albums", store.albums);
    components.push(albums);
  }

  if (store.eps.length > 0) {
    const eps = createAbumComponent("EPs", store.eps);
    components.push(eps);
  }

  if (store.singles.length > 0) {
    const singles = createAbumComponent("Singles", store.singles);
    components.push(singles);
  }

  if (store.appearances.length > 0) {
    const appearances = createAbumComponent("Appearances", store.appearances);
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
