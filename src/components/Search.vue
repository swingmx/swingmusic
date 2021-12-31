<template>
  <div
    class="right-search"
    ref="searchComponent"
  >
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
        <div class="result-item" v-for="song in songs" :key="song">
          <div class="album-art image"></div>
          <div class="tags">
            <span class="title">{{ song.title }}</span>
            <hr />
            <span class="artist">{{ song.artist }}</span>
          </div>
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

export default {

  emits: ["expandSearch", "collapseSearch"],
  props: ["search"],
  setup(props, { emit }) {
    const songs = [
      {
        title: "Thriller",
        artist: "Michael jackson",
      },
      {
        title: "We are the world",
        artist: "Michael jackson",
      },
    ];
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
        title: "🈁 Here",
        icon: "🈁",
      }
    ];
    const searchComponent = ref(null);
    const filters = ref(state.filters);
    const albums = [
      "Smooth Criminal like wtf ... and im serious",
      "Xscape",
      "USA for Africa",
    ];

    const artists = ["Michael Jackson waihenya", "Jackson 5"];
    const query = ref(state.searh_query);
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
          console.log(query.value);
          state.magic_flag.value = false;
        }
      }, 300);
    }

    watch(query, (new_query) => {
      state.search_query.value = new_query;
      if (new_query !== "") {
        counter = 0;
        emit("expandSearch");
      } else {
        emit("collapseSearch");
      }
    });

    onMounted(() => {
      const dom = document.getElementsByClassName("right-search")[0]

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
      songs,
      albums,
      artists,
      query,
      is_hidden,
      magic_flag,
      options,
      filters,
      searchComponent,
    };
  },
};
</script>

<style lang="scss">
.right-search .v0 {
  max-height: 0em;
  transition: max-height 0.5s ease;
}

.right-search .v1 {
  max-height: 26rem;
  transition: max-height 0.5s ease;
}

.right-search {
  position: relative;
  border-radius: 1rem;
  margin: 0.5rem 0 0 0;
  padding: $small $small 0 0;
  background-color: #000000;
  overflow: hidden;

  .item {
    position: relative;
    background-color: rgb(39, 37, 37);
    padding: 0.5rem;
    border-radius: 0.5rem;
    cursor: pointer;
    margin: 0 $small 0 0;
    display: flex;
    align-items: center;

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
    right: 0;

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
  padding: 1rem;
  display: flex;
  align-items: center;
  .more {
    position: absolute;
    right: 1rem;
    padding: 0.5rem;
    user-select: none;
  }

  .more:hover {
    background: $blue;
    border-radius: 0.5rem;
    cursor: pointer;
  }
}

.right-search input {
  width: 100%;
  height: 2.5rem;
  border: none;
  border-radius: 0.5rem;
  background-color: transparent;
  color: rgba(255, 255, 255, 0.479);
  font-size: 1rem;
  line-height: 3rem;
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

/*  */

.right-search .tracks-results {
  border-radius: 0.5rem;
  background-color: rgb(27, 26, 26);
  margin-left: $small;
  padding: $small;

  .result-item {
    display: flex;
    align-items: center;
    height: 4.5rem;
    width: 100%;
    background-color: rgba(20, 20, 20, 0.479);

    .album-art {
      width: 3.5rem;
      height: 3.5rem;
      background-color: rgb(27, 150, 74);
      border-radius: 0.5rem;
      margin: 0 $small 0 $small;
      background-image: url(../assets/images/thriller.jpg);
    }

    .tags .artist {
      font-size: small;
      color: rgba(255, 255, 255, 0.63);
    }

    &:nth-child(odd) {
      background-color: transparent;
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

/*  */

.right-search .albums-results {
  border-radius: 0.5rem;
  background-color: rgb(27, 26, 26);
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
      background-color: rgb(24, 23, 23);
      margin-bottom: 1rem;

      .album-art {
        height: 7rem;
        width: 7rem;
        background-color: rgba(26, 26, 26, 0.452);
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        background-image: url(../assets/images/thriller.jpg);
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

/*  */

.right-search .artists-results {
  border-radius: 0.5rem;
  background-color: rgb(27, 26, 26);
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
      background-color: rgb(24, 23, 23);
      margin-bottom: 1rem;

      .image {
        height: 7rem;
        width: 7rem;
        border-radius: 50%;
        background-color: rgba(16, 65, 14, 0.356);
        margin-bottom: 0.5rem;
        background-size: 50%;
        background-image: url(../assets/images/thriller.jpg);
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