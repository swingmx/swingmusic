<template>
  <div class="folder">
    <div class="table rounded" ref="songtitle" v-if="searchSongs.length">
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
            :searchSongs="searchSongs"
            :songTitleWidth="songTitleWidth"
            :minWidth="minWidth"
            v-for="song in searchSongs"
            :key="song"
            :song="song"
            :current="current"
            :class="{ current: current._id == song._id }"
            @updateQueue="updateQueue"
          />
        </tbody>
      </table>
    </div>
    <div ref="songtitle" v-else-if="searchSongs.length === 0 && search_query">
      <div class="no-results">
        <div class="icon"></div>
        <div class="text">❗ Track not found!</div>
      </div>
    </div>
    <div v-else ref="songtitle"></div>
  </div>
</template>

<script>
import { computed, ref, toRefs } from "@vue/reactivity";
import { onMounted, onUnmounted } from "@vue/runtime-core";

import SongItem from "../SongItem.vue";
import perks from "@/composables/perks.js";
import state from "@/composables/state.js";

export default {
  props: ["songs"],
  components: {
    SongItem,
  },
  setup(props) {
    const song_list = toRefs(props).songs;
    const songtitle = ref(null);
    const songTitleWidth = ref(null);

    const minWidth = ref(300);

    const resizeSongTitleWidth = () => {
      try {
        let a = songtitle.value.clientWidth;

        songTitleWidth.value = a > minWidth.value * 4 ? a / 4 : a / 3;
      } catch (error) {
        return;
      }
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

    const current = ref(perks.current);
    const search_query = ref(state.search_query);

    const updateQueue = async (song) => {
      if (state.queue.value[0]._id.$oid !== song_list.value[0]._id.$oid) {
        const new_queue = song_list.value;
        localStorage.setItem("queue", JSON.stringify(new_queue));
        state.queue.value = new_queue;
      }

      state.current.value = song;
      localStorage.setItem("current", JSON.stringify(song));
    };

    const searchSongs = computed(() => {
      const songs = [];

      if (search_query.value.length > 2) {
        state.loading.value = true;
        
        for (let i = 0; i < song_list.value.length; i++) {
          if (
            song_list.value[i].title
              .toLowerCase()
              .includes(search_query.value.toLowerCase())
          ) {
            songs.push(song_list.value[i]);
          }
        }

        state.loading.value = false;

        return songs;
      } else {
        return song_list.value;
      }
    });

    return {
      searchSongs,
      updateQueue,
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
  background-image: url(../../assets/icons/file.svg);
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