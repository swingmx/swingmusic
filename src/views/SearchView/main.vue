<template>
  <div class="search-view content-page" style="padding-right: 0;">
    <div ref="page" class="page no-scroll" v-auto-animate>
      <component :is="component" />
    </div>
    <button
      class="load-more"
      :class="{ 'btn-disabled': !canLoadMore }"
      @click="loadMore"
    >
      Load more
    </button>
  </div>
</template>

<script setup lang="ts">
import { Routes } from "@/router/routes";
import useSearchStore from "@/stores/search";
import { focusElemByClass } from "@/utils";
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import AlbumPage from "./albums.vue";
import ArtistPage from "./artists.vue";
import TracksPage from "./tracks.vue";

// width of album and artist cards
const defaultItemCount = 6;
const gridItemWidth = 160;
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
  focusElemByClass("page-bottom-padding", 100);
}

function getGridRowItemCount() {
  if (page.value?.offsetWidth === undefined) return defaultItemCount;
  const page_width = page.value?.offsetWidth - 16;
  return Math.floor(page_width / gridItemWidth);
}

function scrollToGridPageBottom() {
  const elem = document.getElementsByClassName("grid-page")[0] as HTMLElement;
  setTimeout(() => {
    elem.scrollTo(0, elem.scrollHeight);
  }, 250);

  // const elemWidth = elem.offsetWidth;
  // console.log(Math.floor(elemWidth / 160));
  // elem.scroll({
  //   top: elem.scrollHeight,
  //   behavior: "smooth",
  // });
}

function loadAlbums() {
  scrollToGridPageBottom();

  setTimeout(() => {
    // search.loadAlbums();
    const itemCount = getGridRowItemCount();
    search.loadAlbums(itemCount);
  
    scrollToGridPageBottom();
  }, 250);

}

function loadArtists() {
  // const itemCount = getGridRowItemCount();
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
});
</script>

<style lang="scss">
.search-view {
  height: calc(100% - 1rem);
  display: grid;
  gap: 1rem;
  grid-template-rows: 1fr max-content;

  margin-right: -0.75rem;

  .page.no-scroll {
    overflow-x: visible;
  }

  .grid-page {
    max-height: 100%;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr));
    gap: 1.75rem 0;

    padding-bottom: 4rem;
    overflow: auto;
    padding-right: $medium;
  }

  button.load-more {
    width: 10rem;
    margin: 0 auto;
  }
}
</style>
