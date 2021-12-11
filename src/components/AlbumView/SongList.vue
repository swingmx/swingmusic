<template>
  <div class="folder" id="p-table">
    <div class="table rounded"  ref="songtitle">
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

    const minWidth = ref(300);

    const songs = Songs.songs;

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

    return { songtitle, songTitleWidth, songs, minWidth };
  },
};
</script>

<style lang="scss">
#p-table {
  height: calc(100% - 0rem) !important;
  overflow: hidden;
  padding-bottom: 0rem;

  table {    
    &::-webkit-scrollbar {
      display: none;
    }

    th {
      position: sticky;
      background-color: rgb(58, 57, 57);
      top: 0;
      z-index: 5;
    }
  }
}
</style>