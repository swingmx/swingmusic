<template>
  <div class="search-view content-page" style="padding-right: 0">
    <div ref="page" class="page no-scroll" v-auto-animate>
      <component :is="component" />
    </div>
    <button
      v-if="$route.params.page !== 'tracks'"
      class="load-more"
      :class="{ load_disabled: !canLoadMore }"
      @click="canLoadMore && loadMore()"
    >
      Load more
    </button>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { computed, onMounted, ref } from "vue";

import useSearchStore from "@/stores/search";

import AlbumPage from "./albums.vue";
import ArtistPage from "./artists.vue";
import TracksPage from "./tracks.vue";

const page = ref<HTMLElement>();

const search = useSearchStore();

enum pages {
  tracks = "tracks",
  albums = "albums",
  artists = "artists",
}

const route = useRoute();

const component = computed(() => {
  switch (route.params.page) {
    case pages.tracks:
      return TracksPage;
    case pages.albums:
      return AlbumPage;

    case pages.artists:
      return ArtistPage;

    default:
      return TracksPage;
  }
});

function loadTracks() {
  search.loadTracks();
}

function scrollToGridPageBottom() {
  const elem = document.getElementsByClassName("grid-page")[0] as HTMLElement;
  setTimeout(() => {
    elem.scroll({
      top: elem.scrollHeight,
      behavior: "smooth",
    });
  }, 250);
}

function loadAlbums() {
  search.loadAlbums();
  scrollToGridPageBottom();
}

function loadArtists() {
  search.loadArtists();

  scrollToGridPageBottom();
}

function loadMore() {
  switch (route.params.page) {
    case pages.tracks:
      loadTracks();
      break;
    case pages.albums:
      loadAlbums();
      break;

    case pages.artists:
      loadArtists();
      break;
    default:
      break;
  }
}

const canLoadMore = computed(() => {
  switch (route.params.page) {
    case pages.tracks:
      return search.tracks.more;
    case pages.albums:
      return search.albums.more;
    case pages.artists:
      return search.artists.more;
    default:
      false;
  }
});

onMounted(() => {
  search.switchTab(route.params.page as string);
  search.query = route.query.q as string;
});
</script>

<style lang="scss">
.search-view {
  height: calc(100%);
  display: grid;
  margin-right: -0.75rem;
  position: relative;

  .page.no-scroll {
    overflow-x: visible;
  }

  .grid-page {
    max-height: 100%;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
    gap: 1.75rem 0;

    padding-bottom: 4rem;
    overflow: auto;
    padding-right: $medium;
    scrollbar-gutter: stable;
  }

  button.load-more {
    position: absolute;
    bottom: 0;
    height: 3rem;
    left: -1.25rem;
    width: calc(100% + 1.25rem);
    border-radius: 0;
    background: $darkestblue;
  }
}


</style>
