<template>
  <div class="right-search">
    <Options />
    <!-- </div> -->
    <div class="scrollable" ref="search_thing">
      <TracksGrid
        v-if="tracks.tracks.length"
        :more="tracks.more"
        :tracks="tracks.tracks"
        @loadMore="loadMoreTracks"
      />
      <div class="separator no-border" v-if="tracks.tracks.length"></div>

      <AlbumGrid
        v-if="albums.albums.length"
        :albums="albums.albums"
        :more="albums.more"
        @loadMore="loadMoreAlbums"
      />
      <div class="separator no-border" v-if="albums.albums.length"></div>
      <ArtistGrid
        v-if="artists.artists.length"
        :artists="artists.artists"
        :more="artists.more"
        @loadMore="loadMoreArtists"
      />
      <div
        v-if="search.query.trim().length === 0"
        class="no-res border rounded"
      >
        <div class="no-res-text">🦋 Find your music</div>
      </div>
      <div
        v-else-if="
          !artists.artists.length &&
          !tracks.tracks.length &&
          !albums.albums.length
        "
        class="no-res border rounded"
      >
        <div class="no-res-text">
          No results for
          <span class="highlight rounded">{{ search.query }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "@vue/reactivity";

import state from "@/composables/state";
import searchMusic from "@/composables/searchMusic.js";
import useDebouncedRef from "@/composables/useDebouncedRef";
import AlbumGrid from "@/components/Search/AlbumGrid.vue";
import ArtistGrid from "@/components/Search/ArtistGrid.vue";
import TracksGrid from "@/components/Search/TracksGrid.vue";
import Options from "@/components/Search/Options.vue";
import loadMore from "../../composables/loadmore";
import useSearchStore from "../../stores/gsearch";
import useTabStore from "../../stores/tabs";

import "@/assets/css/Search/Search.scss";

const search = useSearchStore();
const tabs = useTabStore();

const search_thing = ref(null);

const tracks = reactive({
  tracks: [],
  more: false,
});

let albums = reactive({
  albums: [],
  more: false,
});

const artists = reactive({
  artists: [],
  more: false,
});

const query = useDebouncedRef("", 600);

function scrollSearchThing() {
  search_thing.value.scroll({
    top: search_thing.value.scrollTop + 330,
    left: 0,
    behavior: "smooth",
  });
}

function loadMoreTracks(start) {
  scrollSearchThing();
  loadMore.loadMoreTracks(start).then((response) => {
    tracks.tracks = [...tracks.tracks, ...response.tracks];
    tracks.more = response.more;
  });
}

function loadMoreAlbums(start) {
  loadMore.loadMoreAlbums(start).then((response) => {
    albums.albums = [...albums.albums, ...response.albums];
    albums.more = response.more;
  });
}

function loadMoreArtists(start) {
  scrollSearchThing();
  loadMore.loadMoreArtists(start).then((response) => {
    artists.artists = [...artists.artists, ...response.artists];
    artists.more = response.more;
  });
}

search.$subscribe((mutation, state) => {
  if (state.query.trim() == "") {
    tracks.tracks = [];
    albums.albums = [];
    artists.artists = [];
    return;
  }

  searchMusic(state.query).then((res) => {
    if (tabs.current !== tabs.tabs.search) {
      tabs.switchToSearch();
    }

    albums.albums = res.albums.albums;
    albums.more = res.albums.more;

    artists.artists = res.artists.artists;
    artists.more = res.artists.more;

    tracks.tracks = res.tracks.tracks;
    tracks.more = res.tracks.more;
  });
});
</script>

<style lang="scss">
.right-search {
  position: relative;
  display: grid;
  grid-template-rows: min-content 1fr;
  overflow: hidden;
  width: auto;
  height: 100%;
  padding: $small $small 0 0;

  .no-res {
    text-align: center;
    display: grid;
    height: calc(100% - $small);
    place-items: center;
    font-size: 2rem;
    transition: all 0.3s ease;
    line-height: 4rem !important;

    .highlight {
      padding: $small;
      background-color: rgb(29, 26, 26);
    }
  }

  .heading {
    padding: $medium;
    border-radius: $small;
    margin-bottom: $small;
    font-size: 2rem;
    color: $white;
  }

  .input {
    display: flex;
    align-items: center;
    position: relative;
  }
}

.right-search .scrollable {
  overflow-y: auto;
  scrollbar-width: none;

  &::-webkit-scrollbar {
    display: none;
  }
}
</style>
