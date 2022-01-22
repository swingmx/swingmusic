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
        <div class="loader" v-if="loading"></div>
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
      <div class="tracks-results border" v-if="songs.tracks">
        <div class="heading">TRACKS</div>
        <div class="items">
          <table>
            <tbody>
              <SongItem v-for="song in songs.tracks" :key="song" :song="song" />
            </tbody>
          </table>
          <div class="more" v-if="songs.more">
            <button>
              <div class="text">Load All</div>
            </button>
          </div>
        </div>
      </div>
      <!--  -->
      <div class="albums-results border">
        <div class="heading">ALBUMS <span class="more">SEE ALL</span></div>
        <div class="grid">
          <div
            class="result-item border"
            v-for="album in albums.albums"
            :key="album"
          >
            <div
              class="album-art image"
              :style="{
                backgroundImage: `url('${album.image}')`,
              }"
            ></div>
            <div class="title ellip">{{ album.name }}</div>
            <div class="artistsx ellipsis">
              <span v-for="artist in putCommas(album.artists)" :key="artist">{{
                artist
              }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="separator no-border"></div>
      <!--  -->
      <!-- <div class="artists-results border" v-if="artists">
        <div class="heading">ARTISTS <span class="more">SEE ALL</span></div>
        <div class="grid">
          <div
            class="result-item border"
            v-for="artist in artists.artists"
            :key="artist"
          >
            <div
              class="image"
              :style="{
                backgroundImage: `url(${artist.image})`,
              }"
            ></div>
            <div class="title ellip">{{ artist.name }}</div>
          </div>
        </div>
      </div> -->
    </div>
  </div>
</template>

<script>
import { ref, toRefs } from "@vue/reactivity";

import { onMounted, watch } from "@vue/runtime-core";
import state from "@/composables/state.js";
import searchMusic from "@/composables/searchMusic.js";
import useDebouncedRef from "@/composables/useDebouncedRef";
import SongItem from "@/components/shared/SongItem.vue";
import perks from "@/composables/perks.js";

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
    ];

    const loading = ref(state.loading);
    const searchComponent = ref(null);
    const filters = ref([]);

    const albums = ref([]);
    const artists = ref([]);

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
        albums.value = res.albums;
        artists.value = res.artists;
        state.search_tracks.value = res.tracks;
        // console.log(albums.value)
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
      // const dom = document.getElementsByClassName("right-search")[0];
      // document.addEventListener("click", (e) => {
      //   var isClickedInside = dom.contains(e.target);
      //   if (!isClickedInside) {
      //     emit("collapseSearch");
      //   }
      // });
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
      putCommas: perks.putCommas,
    };
  },
};
</script>

<style lang="scss">
.loader {
  position: absolute;
  right: 0.65rem;
  top: 0.65rem;
  width: 1.5rem;
  height: 1.5rem;
  border: dotted $blue;
  border-radius: 50%;
  animation: spin 0.25s linear infinite;

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
  width: auto;

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
    transform: translateY(-4rem);
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
    cursor: pointer;
  }
}

.right-search {
  .input-loader {
    width: 100%;
    border-radius: 0.4rem;
    position: relative;

    input {
      width: calc(100% - 6rem);
      border: none;
      line-height: 2.5rem;
      background-color: transparent;
      color: rgb(255, 255, 255);
      font-size: 1rem;
      outline: none;
      transition: all 0.5s ease;
      padding-left: $small;

      &:focus {
        transition: all 0.5s ease;
        color: rgb(255, 255, 255);
        outline: none;

        &::placeholder {
          display: none;
        }
      }
    }
  }
}

/* tracks */

.right-search .tracks-results {
  border-radius: 0.5rem;
  margin-left: $small;
  padding: $small;

  .more {
    display: grid;
    place-items: center;
    margin-top: $small;

    button {
      height: 2.5rem;
      width: 10rem;
      display: grid;
    }
  }

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
  width: calc(100% - $small);
  border-radius: 0.5rem;

  background: #0f131b44;

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
      text-align: left !important;
      margin-bottom: 1rem;
      width: 9rem;

      .album-art {
        height: 7rem;
        width: 7rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        background-image: url("../assets/images/null.webp");
      }

      .title {
        width: 7rem;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
      }

      .artistsx {
        width: 7rem;
        display: flex;
        font-size: 0.8rem;
        text-align: left;
        color: rgba(40, 116, 216, 0.767);
      }
    }
  }
}

/* artits */

.right-search .artists-results {
  width: calc(100% - $small);

  border-radius: 0.5rem;
  background: #1214178c;
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