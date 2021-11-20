<template>
  <div class="folder">
    <div class="table" ref="songtitle">
      <table>
        <tr>
          <th>Track</th>
          <th>Artist</th>
          <th>Album</th>
          <th v-if="songTitleWidth > minWidth">Duration</th>
        </tr>
        <tr v-for="song in songs" :key="song">
          <td class="flex">
            <div class="album-art rounded"></div>
            <div class="title-artist">
              <span :style="{ width: songTitleWidth + 'px' }">{{
                song.title
              }}</span>
            </div>
          </td>
          <td :style="{ width: songTitleWidth + 'px' }"><span class="artist" v-for="artist in song.artists" :key="artist">{{ artist}}</span></td>
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
import Songs from '../../data/songs.js'

export default {
  setup() {
    const songtitle = ref(null);
    const songTitleWidth = ref(null);

    const minWidth = ref(250);

    const songs = Songs.songs

    const resizeSongTitleWidth = () => {
      songTitleWidth.value = songtitle.value.clientWidth / 3;
      console.log(songtitle.value.clientWidth / 3);
    };

    onMounted(() => {
      window.addEventListener("resize", () => {
        resizeSongTitleWidth();
      });
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
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.folder .table .flex {
  align-items: center;
  justify-content: flex-start;
}

.folder .table .flex span {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

td,
th {
  text-align: left;
  padding: 8px;
}
th {
  text-transform: uppercase;
  font-weight: normal;
}
tr {
  border-bottom: 1px solid var(--seperator);
}

.folder {
  padding-bottom: 1em;
  margin-bottom: 1em;
}

td .artist {
  color: #b1b1b1fd;
  font-weight: lighter;
  margin-right: 0.5em;
}
</style>