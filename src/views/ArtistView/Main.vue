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
// import Albums from "@/components/ArtistView/Albums.vue";
import useArtistPageStore from "@/stores/pages/artist";
import ArtistAlbums from "@/components/AlbumView/ArtistAlbums.vue";

import { computed } from "vue";
import { onBeforeRouteUpdate } from "vue-router";

const artistStore = useArtistPageStore();

interface ScrollerItem {
  id: string | number;
  component: any;
  props?: Record<string, unknown>;
  // size: number;
}

const header: ScrollerItem = {
  id: "artist-header",
  component: Header,
  // size: 16 * 19,
};

const top_tracks: ScrollerItem = {
  id: "artist-top-tracks",
  component: TopTracks,
  // size: 16 * 25,
};

const artistAlbums: ScrollerItem = {
  id: "artist-albums",
  component: ArtistAlbums,
  // size: 16 * 16,
  props: { title: "Albums", albums: artistStore.albums },
};

const scrollerItems = computed(() => {
  return [header, top_tracks, artistAlbums];
});

onBeforeRouteUpdate((to, from, next) => {
  artistStore.getData(to.params.hash as string);
});
</script>

<style lang="scss">
.section-title {
  margin: 1rem;
  padding-left: 1rem;
}
</style>
