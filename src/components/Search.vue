<template>
  <div class="right-search border" ref="searchComponent">
    <div class="input">
      <div class="search-icon image"></div>
      <div class="filter">
        <div
          class="item"
          v-for="filter in filters"
          :key="filter"
          @click="removeFilter(filter)"
        >
          {{ filter }}<span class="cancel image"></span>
        </div>
      </div>
      <input
        type="search"
        id="search"
        @focus="activateMagicFlag"
        @blur="removeMagicFlag"
        @keyup.backspace="removeLastFilter"
        placeholder="find your music"
        v-model="query"
      />
      <div class="loader" v-if="loading"></div>
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
    <div class="options" v-if="magic_flag">
      <div class="item info">Filter by:</div>
      <div
        class="item"
        v-for="option in options"
        :key="option"
        @click="addFilter(option.icon)"
      >
        {{ option.title }}
      </div>
    </div>
    <div class="scrollable" :class="{ v0: !is_hidden, v1: is_hidden }">
      <div class="tracks-results">
        <div class="heading">TRACKS<span class="more">SEE ALL</span></div>
        <div class="items">
          <table>
            <thead></thead>
            <tbody>
              <SongItem v-for="song in songs" :key="song" :song="song" />
            </tbody>
          </table>
        </div>
      </div>
      <!--  -->
      <div class="albums-results">
        <div class="heading">ALBUMS <span class="more">SEE ALL</span></div>
        <div class="grid">
          <div class="result-item" v-for="album in albums" :key="album">
            <div class="album-art image"></div>
            <div class="title ellip">{{ album }}</div>
          </div>
        </div>
      </div>
      <div class="separator no-border"></div>
      <!--  -->
      <div class="artists-results" v-if="artists">
        <div class="heading">ARTISTS <span class="more">SEE ALL</span></div>
        <div class="grid">
          <div class="result-item" v-for="artist in artists" :key="artist">
            <div class="image"></div>
            <div class="title ellip">{{ artist }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, toRefs } from "@vue/reactivity";

import { onMounted, watch } from "@vue/runtime-core";
import state from "@/composables/state.js";
import searchMusic from "../composables/searchMusic.js";
import useDebouncedRef from "@/composables/useDebouncedRef";
import SongItem from "@/components/SongItem.vue";

export default {
  emits: ["expandSearch", "collapseSearch"],
  props: ["search"],
  components: {
    SongItem,
  },
  setup(props, { emit }) {
    const options = [
      {
        title: "🎵 Track",
        icon: "🎵",
      },
      {
        title: "💿 Album",
        icon: "💿",
      },
      {
        title: "🙄 Artist",
        icon: "🙄",
      },
      {
        title: "😍 Playlist",
        icon: "😍",
      },
      {
        title: "📁 Folder",
        icon: "📁",
      },
      {
        title: "🈁 This folder",
        icon: "🈁",
      },
    ];

    const loading = ref(state.loading);
    const searchComponent = ref(null);
    const filters = ref(state.filters);
    const albums = [
      "Smooth Criminal like wtf ... and im serious",
      "Xscape",
      "USA for Africa",
    ];

    const artists = ["Michael Jackson waihenya", "Jackson 5"];
    const query = useDebouncedRef("", 400);
    const magic_flag = ref(state.magic_flag);
    const is_hidden = toRefs(props).search;

    function addFilter(filter) {
      if (!filters.value.includes(filter)) {
        state.filters.value.push(filter);
      }
    }

    function removeFilter(filter) {
      state.filters.value = filters.value.filter((f) => f !== filter);
    }

    let counter = 0;

    function removeLastFilter() {
      if (query.value === "" || query.value === null) {
        counter++;

        if (counter > 1 || query.value === null) {
          state.filters.value.pop();
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
      searchMusic(new_query);

      state.search_query.value = new_query;
      if (new_query !== "") {
        counter = 0;
        if (!filters.value.includes("🈁")) {
          emit("expandSearch");
        }
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
      songs: state.search_tracks,
      albums,
      artists,
      query,
      is_hidden,
      magic_flag,
      options,
      filters,
      searchComponent,
      loading,
      searchMusic,
    };
  },
};
</script>

<style lang="scss">
.loader {
  position: absolute;
  right: 0;
  width: 2rem;
  height: 2rem;
  border: solid #fff;
  border-radius: 50%;
  border-bottom: solid rgb(255, 174, 0);
  border-top: solid rgb(255, 174, 0);
  animation: spin 0.3s linear infinite;

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
}
.right-search .v0 {
  max-height: 0em;
  transition: max-height 0.5s ease;
}

.right-search .v1 {
  max-height: 25rem;
  transition: max-height 0.5s ease;
}

.right-search {
  position: relative;
  border-radius: $small;
  margin: 0.5rem 0 0 0;
  padding: 1rem $small 0 0;
  background-color: $card-dark;
  overflow: hidden;

  .item {
    position: relative;
    background-color: rgba(34, 33, 33, 0.637);
    padding: 0.5rem;
    border-radius: 0.5rem;
    cursor: pointer;
    margin: 0 $small 0 0;
    display: flex;
    align-items: center;
    font-size: 0.9rem;
    color: rgb(250, 250, 250);

    &:hover {
      background-color: rgb(170, 50, 50);
    }
  }

  .input {
    display: flex;
    align-items: center;
    position: relative;

    .filter {
      display: flex;
      margin-left: 3rem;
      height: 2rem;
      // border: solid;

      .item {
        &:hover {
          width: 4rem;

          .cancel {
            position: absolute;
            right: 0.5rem;
            width: 1.5rem;
            height: 1.5rem;
            background-image: url(../assets/icons/a.svg);
            background-size: 70%;
          }
        }
      }
    }
  }

  .search-icon {
    position: absolute;
    height: 2.5rem;
    width: 2.5rem;
    background-image: url(../assets/icons/search.svg);
    background-size: 70%;
  }

  .v11 {
    opacity: 0;
    transform: translateY(-3rem);
    transition: all 0.2s ease-in;
  }

  .v00 {
    opacity: 1;
    transition: all 0.2s ease-in;
  }

  .suggestions {
    display: flex;
    gap: 0.5rem;
    margin-left: 1rem;
    position: absolute;
    right: 2.5rem;

    .item::before {
      content: "#";
      color: grey;
    }
  }
}

.right-search .options {
  display: flex;

  .item {
    margin: $small;
  }
}

.right-search .scrollable {
  height: 26rem;
  overflow-y: auto;
  scroll-behavior: smooth;
  padding: 0 $small 0 0;
  margin-bottom: 0.5rem;
}

.right-search .heading {
  font-size: small;
  position: relative;
  padding: $small;
  display: flex;
  align-items: center;

  .more {
    position: absolute;
    right: $small;
    padding: 0.5rem;
    user-select: none;
  }

  .more:hover {
    // background: $blue;
    // border-radius: 0.5rem;
    cursor: pointer;
  }
}

.right-search input {
  width: calc(100% - 6rem);
  border: none;
  border-radius: 0.5rem;
  background-color: transparent;
  color: rgb(255, 255, 255);
  font-size: 1rem;
  outline: none;
  transition: all 0.5s ease;
}
.right-search input:focus {
  transition: all 0.5s ease;
  color: rgb(255, 255, 255);
  outline: none;

  &::placeholder {
    display: none;
  }
}

/* tracks */

.right-search .tracks-results {
  border-radius: 0.5rem;
  // background: #ca0377;
  margin-left: $small;
  padding: $small;
  // border: solid;

  .items {
    border-radius: $small;
    background-color: $card-dark;
  }

  .result-item {
    display: flex;
    align-items: center;
    height: 4.5rem;
    width: 100%;

    .album-art {
      width: 3.5rem;
      height: 3.5rem;
      background-color: rgb(27, 150, 74);
      border-radius: 0.5rem;
      margin: 0 $small 0 $small;
      background-image: url(../assets/images/null.webp);
    }

    .tags .artist {
      font-size: small;
      color: rgba(255, 255, 255, 0.63);
    }

    &:hover {
      background-color: $blue;
      border-radius: $small;
    }
  }
}

.right-search hr {
  margin: 0.1rem;
  border: none;
}

/* albums */

.right-search .albums-results {
  border-radius: 0.5rem;

  background: #011327;

  margin-left: $small;
  margin-top: $small;

  .grid {
    display: flex;
    flex-wrap: wrap;
    padding: 0 0 0 $small;
    gap: $small;

    .result-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: $small;
      border-radius: $small;
      background-color: $card-dark;
      margin-bottom: 1rem;

      .album-art {
        height: 7rem;
        width: 7rem;
        background-color: rgba(26, 26, 26, 0.452);
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        background-image: url("../assets/images/null.webp");
      }

      .title {
        width: 7rem;
        text-align: center;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
      }
    }
  }
}

/* artits */

.right-search .artists-results {
  border-radius: 0.5rem;
  background: #381900;
  margin: 0 0 0 $small;

  .grid {
    padding: 0 0 0 $small;
    display: flex;
    gap: 1rem;

    .result-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: $small;
      border-radius: $small;
      background-color: $card-dark;
      margin-bottom: 1rem;

      .image {
        height: 7rem;
        width: 7rem;
        border-radius: 50%;
        background-color: rgba(16, 65, 14, 0.356);
        margin-bottom: 0.5rem;
        background-size: 50%;
        background-image: url("../assets/images/null.webp");
        background-size: cover;
      }

      .title {
        width: 7rem;
        text-align: center;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
      }
    }
  }
}
</style>