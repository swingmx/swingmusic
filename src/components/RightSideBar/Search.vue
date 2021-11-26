<template>
  <div class="right-search">
    <input type="search" id="search" placeholder="Michael Jackson" />
    <div class="scrollable">

      <div class="tracks-results">
      <h3 class="heading">TRACKS <span class="more">SEE ALL</span></h3>
        <div class="result-item" v-for="song in songs" :key="song">
          <div class="album-art image"></div>
          <div class="tags">
            <span class="title">{{ song.title }}</span>
            <hr />
            <span class="artist">{{ song.artist }}</span>
          </div>
        </div>
      </div>
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

      <div class="artists-results" v-if="artists">
        <h3 class="heading">ARTISTS <span class="more" v-if="artists.length>3">SEE ALL</span></h3>
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
export default {
  setup() {
    const songs = [
      {
        title: "Thriller",
        artist: "Michael jackson",
      },
      {
        title: "We are the world",
        artist: "Michael jackson",
      },
      {
        title: "Thriller",
        artist: "Michael jackson",
      },
      {
        title: "We are the world",
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

    const artists = ["Michael Jackson", "Jackson 5"]

    return { songs, albums, artists };
  },
};
</script>

<style>
.right-search {
  position: relative;
  height: 30em;
  border-radius: 1em;
  margin: 0.5em 0 0 0;
  padding: 0.75em;
  background-color: rgba(32, 31, 31, 0.5);
  overflow: hidden;
}

.right-search .scrollable {
  height: calc(100% - 4em);
  overflow-y: scroll;
  scroll-behavior: smooth;
}

.right-search .scrollable::-webkit-scrollbar {
  display: none;
}

.right-search .heading {
  font-size: small;
  position: relative;
  padding: 1em;
  display: flex;
  align-items: center;
}

.right-search .heading .more {
  position: absolute;
  right: 1em;
  padding: 0.5em;
}

.right-search .heading .more:hover {
  background: rgb(62, 69, 77);
  border-radius: 0.5em;
  cursor: pointer;
}
.right-search input {
  width: 100%;
  border: 0.1em solid;
  border-radius: 0.5em;
  padding-left: 1em;
  background-color: transparent;
  color: rgba(255, 255, 255, 0.479);
  font-size: 1em;
  line-height: 3em;
  outline: none;
  margin-bottom: 1em;
}

.right-search input::-webkit-search-cancel-button {
  position: relative;
  right: 1em;
  cursor: pointer;
}

.right-search input:focus {
  color: rgb(255, 255, 255);
}

/*  */

.right-search .tracks-results {
  border-radius: 0.5em;
  overflow: hidden;
}

.right-search .tracks-results .heading {
  padding: 0.5em;
}

.right-search .tracks-results .result-item {
  display: flex;
  align-items: center;
  height: 4.5em;
  background-color: rgba(20, 20, 20, 0.733);
}

.right-search .tracks-results .result-item:nth-child(odd) {
  background-color: rgba(27, 26, 27, 0.589);
}
.right-search .tracks-results .result-item .album-art {
  width: 4em;
  height: 4em;
  background-color: rgb(27, 150, 74);
  border-radius: 0.5em;
  margin: 0 0.5em 0 0.25em;
  background-image: url(../../assets/images/thriller.jpg);
}

.right-search hr {
  margin: 0.1em;
  border: none;
}

.right-search .tracks-results .result-item .tags .artist {
  font-size: small;
  color: rgba(255, 255, 255, 0.63);
}
/*  */

.right-search .albums-results {
  border-radius: 0.5em;
  background-color: rgba(8, 3, 1, 0.274);
  margin-top: 1em;
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
  height: 7em;
  width: 7em;
  background-color: rgba(26, 26, 26, 0.452);
  border-radius: 0.5em;
  margin-bottom: 0.5em;
  background-image: url(../../assets/images/thriller.jpg);
}

.right-search .albums-results .result-item .title {
  width: 7em;
  text-align: center;
  margin-bottom: 0.5em;
}

/*  */

.right-search .artists-results {
  border-radius: 0.5em;
  background-color: rgba(8, 3, 1, 0.274);
}

.right-search .artists-results .grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

.right-search .artists-results .result-item .image {
  height: 7em;
  width: 7em;
  border-radius: 50%;
  background-color: rgba(16, 65, 14, 0.356);
  margin-bottom: 0.5em;
  background-image: url(../../assets/icons/logo-small.svg);
  background-size: 50%;
  background-image: url(../../assets/images/thriller.jpg);
  background-size: cover;
}

.right-search .artists-results .result-item .name {
  width: 7em;
  text-align: center;
  margin-bottom: 0.5em;
}
</style>