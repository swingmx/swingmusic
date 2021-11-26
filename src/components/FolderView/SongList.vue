<template>
  <div class="folder">
    <div class="table rounded" ref="songtitle">
      <table>
        <tr>
          <th>Track</th>
          <th>Artist</th>
          <th>Album</th>
          <th v-if="songTitleWidth > minWidth">Duration</th>
        </tr>
        <tr v-for="song in songs" :key="song">
          <td :style="{ width: songTitleWidth + 'px' }" class="flex">
            <div class="album-art rounded image"></div>
            <div>
              <span class="ellipsis">{{ song.title }}</span>
            </div>
          </td>
          <td :style="{ width: songTitleWidth + 'px' }">
            <span class="artist" v-for="artist in song.artists" :key="artist">{{
              artist
            }}</span>
          </td>
          <td :style="{ width: songTitleWidth + 'px' }">{{ song.album }}</td>
          <td
            :style="{ width: songTitleWidth + 'px' }"
            v-if="songTitleWidth > minWidth"
          >
            {{ song.duration }}
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
import { onMounted, onUnmounted } from "@vue/runtime-core";
import Songs from "../../data/songs.js";

export default {
  setup() {
    const songtitle = ref(null);
    const songTitleWidth = ref(null);

    const minWidth = ref(250);

    const songs = Songs.songs;

    const resizeSongTitleWidth = () => {
      songTitleWidth.value =
        songtitle.value.clientWidth > minWidth.value * 4
          ? songtitle.value.clientWidth / 4
          : (songTitleWidth.value = songtitle.value.clientWidth / 3);
    };

    onMounted(() => {
      resizeSongTitleWidth();
      window.addEventListener("resize", () => {
        resizeSongTitleWidth();
      });
      console.log(songTitleWidth.value);
    });

    onUnmounted(() => {
      window.removeEventListener("resize", () => {
        resizeSongTitleWidth();
      });
    });

    return { songtitle, songTitleWidth, songs, minWidth };
  },
};
</script>

<style>
.table {
  width: 100%;
  background: transparent;
  overflow: hidden;
}

.folder .table table {
  border-collapse: collapse;
  width: 100%;
  text-transform: capitalize;
}

.folder .table table td .album-art {
  width: 3em;
  height: 3em;
  margin-right: 1em;
  background-color: #ccc;
  background-image: url(../../assets/images/Jim_Reeves.png);
}

.folder .table .flex {
  position: relative;
  align-items: center;
}

.folder .table .flex > div > span {
  position: absolute;
  bottom: 1.5em;
  width: calc(100% - 6em);
}

td,
th {
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: rgba(29, 29, 29, 0.767);
}
tr:nth-child(odd) {
  background-color: rgba(56, 56, 56, 0.363);
}

th {
  text-transform: uppercase;
  font-weight: normal;
}

.folder {
  padding-bottom: 1em;
}

td .artist {
  color: #b1b1b1fd;
  font-weight: lighter;
  margin-right: 0.5em;
}
</style>