<template>
  <div class="folder">
    <div class="table rounded" ref="songtitle" v-if="songs.length">
      <table>
        <thead>
          <tr>
            <th>Track</th>
            <th>Artist</th>
            <th>Album</th>
            <th v-if="songTitleWidth > minWidth">Duration</th>
          </tr>
        </thead>
        <tbody>
          <SongItem
            :songTitleWidth="songTitleWidth"
            :minWidth="minWidth"
            v-for="song in songs"
            :key="song"
            :song="song"
            :current="current"
            @updateQueue="updateQueue"
            @loadAlbum="loadAlbum"
          />
        </tbody>
      </table>
    </div>
    <div ref="songtitle" v-else-if="songs.length === 0 && search_query">
      <div class="no-results">
        <div class="icon"></div>
        <div class="text">❗ Track not found!</div>
      </div>
    </div>
    <div v-else ref="songtitle"></div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
import { onMounted, onUnmounted } from "@vue/runtime-core";

import SongItem from "../SongItem.vue";
import getAlbum from "@/composables/getAlbum.js";
import perks from "@/composables/perks.js";
import state from "@/composables/state.js";
import { useRouter, useRoute } from "vue-router";

export default {
  props: ["songs"],
  components: {
    SongItem,
  },
  setup() {
    const songtitle = ref(null);
    const songTitleWidth = ref(null);

    const minWidth = ref(300);
    let routex;

    const current = ref(perks.current);
    const search_query = ref(state.search_query);
    const route = useRouter();

    const resizeSongTitleWidth = () => {
      try {
        let a = songtitle.value.clientWidth;

        songTitleWidth.value = a > minWidth.value * 4 ? a / 4 : a / 3;
      } catch (error) {
        return;
      }
    };

    onMounted(() => {
      routex = useRoute().name;

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

    function updateQueue(song) {
      let type;

      switch (routex) {
        case "FolderView":
            type = "folder";
          break;
        case "AlbumView":
            type = "album";
          break;
      }

      perks.updateQueue(song, type);
    }

    function loadAlbum(title, album_artist) {
      state.loading.value = true;

      getAlbum(title, album_artist).then((data) => {
        state.album_song_list.value = data.songs;
        state.album_info.value = data.info;

        route.push({
          name: "AlbumView",
          params: {
            album: title,
            artist: album_artist,
          },
        });
        state.loading.value = false;
      });
    }

    return {
      updateQueue,
      loadAlbum,
      songtitle,
      songTitleWidth,
      minWidth,
      current,
      search_query,
    };
  },
};
</script>

<style lang="scss">
.no-results {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.table {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  background-color: $card-dark;

  &::-webkit-scrollbar {
    display: none;
  }

  .current * {
    color: rgb(0, 110, 255);
  }

  .current:hover {
    * {
      color: rgb(255, 255, 255);
    }
  }
}

.folder .table table td .album-art {
  width: 3rem;
  height: 3rem;
  margin-right: 1rem;
  background-image: url(../../assets/images/null.webp);
  display: grid;
  place-items: center;
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
  padding: $small 0 $small $small;
  text-align: left;
}

th {
  text-transform: uppercase;
  font-weight: normal;
  display: none;
}

td .artist {
  margin-right: 0.2rem;
}

.folder .table table {
  border-collapse: collapse;
  text-transform: capitalize;
  position: relative;

  tbody tr {
    cursor: pointer;
    transition: all 0.1s ease;

    &:hover {
      & {
        & > td {
          background-color: rgb(5, 80, 150);
        }

        & td:first-child {
          border-radius: $small 0 0 $small;
        }

        & td:last-child {
          border-radius: 0 $small $small 0;
        }
      }
    }
  }
}
</style>