<template>
  <div class="right-search">
    <input
      type="search"
      id="search"
      placeholder="Michael Jackson"
      v-model="query"
    />
    <div class="scrollable" :class="{ v0: !is_hidden, v1: is_hidden }">
      <div class="tracks-results">
        <h3 class="heading">TRACKS<span class="more">SEE ALL</span></h3>
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
        <h3 class="heading">ALBUMS <span class="more">SEE ALL</span></h3>
        <div class="grid">
          <div
            class="result-item result-item3"
            v-for="album in albums"
            :key="album"
          >
            <div class="album-art image"></div>
            <div class="title ellipsis">{{ album }}</div>
          </div>
        </div>
      </div>
      <!--  -->
      <div class="artists-results" v-if="artists">
        <h3 class="heading">
          ARTISTS <span class="more" v-if="artists.length > 3">SEE ALL</span>
        </h3>
        <div class="grid">
          <div
            class="result-item result-item3"
            v-for="artist in artists"
            :key="artist"
          >
            <div class="image"></div>
            <div class="name ellipsis">{{ artist }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, toRefs } from "@vue/reactivity";
import { watch } from "@vue/runtime-core";

export default {
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

    const albums = [
      "Smooth Criminal like wtf ... and im serious",
      "Xscape",
      "USA for Africa",
    ];

    const artists = ["Michael Jackson", "Jackson 5"];

    const query = ref(null);

    const is_hidden = toRefs(props).search;

    watch(query, (new_query) => {
      if (new_query.length > 0) {
        emit("expandSearch");
      } else {
        emit("collapseSearch");
      }
    });

    return { songs, albums, artists, query, is_hidden };
  },
};
</script>

<style>
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
  padding: 0.75rem;
  background-color: #131313b2;
  overflow: hidden;
}

.right-search .scrollable {
  height: 26rem;
  overflow-y: scroll;
  scroll-behavior: smooth;
}

.right-search .scrollable::-webkit-scrollbar {
  display: none;
}

.right-search .heading {
  font-size: small;
  position: relative;
  padding: 1rem;
  display: flex;
  align-items: center;
}

.right-search .heading .more {
  position: absolute;
  right: 1rem;
  padding: 0.5rem;
  user-select: none;
}

.right-search .heading .more:hover {
  background: rgb(62, 69, 77);
  border-radius: 0.5rem;
  cursor: pointer;
}
.right-search input {
  width: 100%;
  border: none;
  border-radius: 0.5rem;
  padding-left: 1rem;
  background-color: #4645456c;
  color: rgba(255, 255, 255, 0.479);
  font-size: 1rem;
  line-height: 3rem;
  outline: none;
  transition: all 0.5s ease;
}
.right-search input:focus {
  transition: all 0.5s ease;
  color: rgb(255, 255, 255);
  outline: 0.1rem solid #fafafa52;
}

.right-search input::-webkit-search-cancel-button {
  position: relative;
  right: 1rem;
  cursor: pointer;
}

/*  */

.right-search .tracks-results {
  border-radius: 0.5rem;
  overflow: hidden;
}

.right-search .tracks-results .heading {
  padding: 0.5rem;
}

.right-search .tracks-results .result-item {
  display: flex;
  align-items: center;
  height: 4.5rem;
  background-color: rgba(20, 20, 20, 0.733);
}

.right-search .tracks-results .result-item:nth-child(odd) {
  background-color: rgba(27, 26, 27, 0.589);
}
.right-search .tracks-results .result-item .album-art {
  width: 4rem;
  height: 4rem;
  background-color: rgb(27, 150, 74);
  border-radius: 0.5rem;
  margin: 0 0.5rem 0 0.25rem;
  background-image: url(../../assets/images/thriller.jpg);
}

.right-search hr {
  margin: 0.1rem;
  border: none;
}

.right-search .tracks-results .result-item .tags .artist {
  font-size: small;
  color: rgba(255, 255, 255, 0.63);
}
/*  */

.right-search .albums-results {
  border-radius: 0.5rem;
  background-color: rgba(8, 3, 1, 0.274);
  margin-top: 1rem;
}

.right-search .albums-results .grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

.right-search .result-item3 {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.right-search .albums-results .result-item .album-art {
  height: 7rem;
  width: 7rem;
  background-color: rgba(26, 26, 26, 0.452);
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
  background-image: url(../../assets/images/thriller.jpg);
}

.right-search .albums-results .result-item .title {
  width: 7rem;
  text-align: center;
  margin-bottom: 0.5rem;
}

/*  */

.right-search .artists-results {
  border-radius: 0.5rem;
  background-color: rgba(8, 3, 1, 0.274);
}

.right-search .artists-results .grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

.right-search .artists-results .result-item .image {
  height: 7rem;
  width: 7rem;
  border-radius: 50%;
  background-color: rgba(16, 65, 14, 0.356);
  margin-bottom: 0.5rem;
  background-image: url(../../assets/icons/logo-small.svg);
  background-size: 50%;
  background-image: url(../../assets/images/thriller.jpg);
  background-size: cover;
}

.right-search .artists-results .result-item .name {
  width: 7rem;
  text-align: center;
  margin-bottom: 0.5rem;
}
</style>