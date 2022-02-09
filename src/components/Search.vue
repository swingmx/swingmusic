<template>
  <div class="right-search border">
    <div>
      <div class="input">
        <Loader/>
        <Filters :filters="filters" @removeFilter="removeFilter"/>
        <div class="input-loader border">
          <input
              id="search"
              v-model="query"
              placeholder="find your music"
              type="text"
              @keyup.backspace="removeLastFilter"
          />
          <div class="search-icon image"></div>
        </div>
      </div>
      <div class="separator no-border"></div>
      <Options @addFilter="addFilter"/>
    </div>
    <div class="scrollable">
      <TracksGrid
          v-if="tracks.tracks.length"
          :more="tracks.more"
          :tracks="tracks.tracks"
      />
      <AlbumGrid
          v-if="albums.albums.length"
          :albums="albums.albums"
          :more="albums.more"
      />
      <div class="separator no-border"></div>
      <ArtistGrid
          v-if="artists.artists.length"
          :artists="artists.artists"
          :more="artists.more"
      />
      <div
          v-if="
          !artists.artists.length &&
          !tracks.tracks.length &&
          !albums.albums.length && query.length != 0
        "
          class="no-res"
      >
        <div class="no-res-text">
          No results for <span class="highlight rounded">{{ query }}</span>
        </div>
      </div>
      <div v-else-if="query.length == 0" class="no-res">
        <div class="no-res-text">Find your music 🔍😀</div>
      </div>
    </div>
  </div>
</template>

<script>
import {reactive, ref} from "@vue/reactivity";

import {watch} from "@vue/runtime-core";
import state from "@/composables/state.js";
import searchMusic from "@/composables/searchMusic.js";
import useDebouncedRef from "@/composables/useDebouncedRef";
import AlbumGrid from "@/components/Search/AlbumGrid.vue";
import ArtistGrid from "@/components/Search/ArtistGrid.vue";
import TracksGrid from "@/components/Search/TracksGrid.vue";
import Loader from "@/components/Search/Loader.vue";
import Options from "@/components/Search/Options.vue";
import Filters from "@/components/Search/Filters.vue";
import "@/assets/css/Search/Search.scss";

export default {
  components: {
    AlbumGrid,
    ArtistGrid,
    TracksGrid,
    Loader,
    Options,
    Filters,
  },

  setup() {
    const loading = ref(state.loading);
    const filters = ref([]);

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

    function addFilter(filter) {
      if (!filters.value.includes(filter)) {
        filters.value.push(filter);
      }
    }

    function removeFilter(filter) {
      filters.value = filters.value.filter((f) => f !== filter);
    }

    let counter = 0;

    function removeLastFilter() {
      if (query.value === "" || query.value === null) {
        counter++;

        if (counter > 1 || query.value === null) {
          filters.value.pop();
        }
      }
    }

    watch(query, (new_query) => {
      if (query.value == "" || query.value == "  " || query.value.length < 2) {
        albums.albums = [];
        artists.artists = [];
        tracks.tracks = [];

        return;
      }
      ;

      searchMusic(new_query).then((res) => {
        albums.albums = res.albums.albums;
        albums.more = res.albums.more;

        artists.artists = res.artists.artists;
        artists.more = res.artists.more;

        tracks.tracks = res.tracks.tracks;
        tracks.more = res.tracks.more;
      });
    });

    return {
      addFilter,
      removeFilter,
      removeLastFilter,
      tracks,
      albums,
      artists,
      query,
      filters,
      loading,

    };
  },
};
</script>
