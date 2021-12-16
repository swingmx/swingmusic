<template>
  <div class="folder">
    <div class="table rounded" ref="songtitle" v-if="songs.length">
      <table class="rounded">
        <tr>
          <th>Track</th>
          <th>Artist</th>
          <th>Album</th>
          <th v-if="songTitleWidth > minWidth">Duration</th>
        </tr>
        <tr v-for="song in songs" :key="song">
          <td :style="{ width: songTitleWidth + 'px' }" class="flex">
            <div
              class="album-art rounded image"
              :style="{
                backgroundImage: `url(&quot;${image_path + song.image}&quot;)`,
              }"
            ></div>
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
            {{ `${Math.trunc(song.length / 60)} min` }}
          </td>
        </tr>
      </table>
    </div>
    <div v-else ref="songtitle"></div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
import { onMounted, onUnmounted } from "@vue/runtime-core";

export default {
  props: ["songs"],
  setup() {
    const songtitle = ref(null);
    console.log(songtitle);
    const songTitleWidth = ref(null);
    const image_path = "http://127.0.0.1:8900/images/thumbnails/";

    const minWidth = ref(300);

    const resizeSongTitleWidth = () => {
      let a = songtitle.value.clientWidth;

      songTitleWidth.value = a > minWidth.value * 4 ? a / 4 : a / 3;
    };

    onMounted(() => {
      resizeSongTitleWidth();

      window.addEventListener("resize", () => {
        resizeSongTitleWidth();
      });
    });

    onUnmounted(() => {
      window.removeEventListener("resize", () => {
        resizeSongTitleWidth();
      });
    });

    return { songtitle, image_path, songTitleWidth, minWidth };
  },
};
</script>

<style lang="scss">
.table {
  width: 100%;
  height: calc(100%);
  background-color: rgba(56, 56, 56, 0.363);
  overflow-y: auto;

  &::-webkit-scrollbar {
    display: none;
  }
}

.folder .table table {
  border-collapse: collapse;
  text-transform: capitalize;
  position: relative;
  margin: 1rem;

  tr {
    &:hover {
      td {
        background-color: rgba(255, 174, 0, 0.534);
      }
    }
  }
}

.folder .table table td .album-art {
  width: 3rem;
  height: 3rem;
  margin-right: 1rem;
  background-image: url(../../assets/icons/file.svg);
}

.folder .table .flex {
  position: relative;
  align-items: center;
}

.folder .table .flex > div > span {
  position: absolute;
  bottom: 1.5rem;
  width: calc(100% - 6rem);
}
td,
th {
  padding: 8px;
  text-align: left;
}

th {
  height: 3rem;
}

tr:nth-child(even) {
  background-color: rgba(29, 29, 29, 0.767);
}

th {
  text-transform: uppercase;
  font-weight: normal;
}

.folder {
  padding-bottom: 1rem;
}

td .artist {
  color: #b1b1b1fd;
  font-weight: lighter;
  margin-right: 0.5rem;
}
</style>