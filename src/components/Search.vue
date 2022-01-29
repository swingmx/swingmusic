<template>
  <div class="right-search border" ref="searchComponent">
    <div class="input">
      <Loader />
      <Filters :filters="filters" @removeFilter="removeFilter" />
      <div class="input-loader border">
        <input
          type="search"
          id="search"
          @focus="activateMagicFlag"
          @blur="removeMagicFlag"
          @keyup.backspace="removeLastFilter"
          placeholder="find your music"
          v-model="query"
        />
        <div class="search-icon image"></div>
        <!--  -->
      </div>
      <div
        class="suggestions v00"
        :class="{
          v00: !filters.length && !query,
          v11: filters.length || query,
        }"
      >
        <div class="item">Kenny Rogers</div>
      </div>
    </div>
    <div class="separator no-border"></div>
    <Options :magic_flag="magic_flag" @addFilter="addFilter" />
    <div class="scrollable" :class="{ v0: !is_hidden, v1: is_hidden }">
      <TracksGrid
        :tracks="tracks.tracks"
        :more="tracks.more"
        v-if="tracks.tracks.length"
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
        class="no-res"
        v-if="
          !artists.artists.length &&
          !tracks.tracks.length &&
          !albums.albums.length
        "
      >
        <div class="no-res-icon image"></div>
        <div class="no-res-text">
          No results for <span class="highlight rounded">{{ query }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref, toRefs } from "@vue/reactivity";

import { onMounted, watch } from "@vue/runtime-core";
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
  emits: ["expandSearch", "collapseSearch"],
  props: ["search"],
  components: {
    AlbumGrid,
    ArtistGrid,
    TracksGrid,
    Loader,
    Options,
    Filters,
  },

  setup(props, { emit }) {
    const loading = ref(state.loading);
    const searchComponent = ref(null);
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

    const query = useDebouncedRef("", 400);
    const magic_flag = ref(state.magic_flag);
    const is_hidden = toRefs(props).search;

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

    function activateMagicFlag() {
      setTimeout(() => {
        state.magic_flag.value = true;
      }, 300);
    }

    function removeMagicFlag() {
      setTimeout(() => {
        if (
          (!filters.value.length && query.value == null) ||
          query.value == ""
        ) {
          state.magic_flag.value = false;
        }
      }, 3000);
    }

    watch(query, (new_query) => {
      searchMusic(new_query).then((res) => {
        albums.albums = res.albums.albums;
        albums.more = res.albums.more;

        artists.artists = res.artists.artists;
        artists.more = res.artists.more;

        tracks.tracks = res.tracks.tracks;
        tracks.more = res.tracks.more;
      });

      state.search_query.value = new_query;
      if (new_query !== "" && new_query.length > 2) {
        counter = 0;
        emit("expandSearch");
      } else {
        emit("collapseSearch");
      }
    });

    onMounted(() => {
      const dom = document.getElementsByClassName("right-search")[0];

      document.addEventListener("click", (e) => {
        var isClickedInside = dom.contains(e.target);
        if (!isClickedInside) {
          emit("collapseSearch");
        }
      });
    });

    return {
      addFilter,
      activateMagicFlag,
      removeMagicFlag,
      removeFilter,
      removeLastFilter,
      tracks,
      albums,
      artists,
      query,
      is_hidden,
      magic_flag,
      filters,
      searchComponent,
      loading,
      searchMusic,
    };
  },
};
</script>
