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
          <tr
            v-for="song in songs"
            :key="song"
            @click="
              updateQueue(song, song.type.name, song.type.id),
                playAudio(song.filepath)
            "
          >
            <td :style="{ width: songTitleWidth + 'px' }" class="flex">
              <div
                class="album-art rounded image"
                :style="{
                  backgroundImage: `url(&quot;${song.image}&quot;)`,
                }"
              ></div>
              <div>
                <span class="ellip">{{ song.title }}</span>
              </div>
            </td>
            <td :style="{ width: songTitleWidth + 'px' }">
              <div class="ellip">
                <span
                  class="artist"
                  v-for="artist in putCommas(song.artists)"
                  :key="artist"
                  >{{ artist }}</span
                >
              </div>
            </td>
            <td :style="{ width: songTitleWidth + 'px' }">
              <div class="ellip">{{ song.album }}</div>
            </td>
            <td
              :style="{ width: songTitleWidth + 'px' }"
              v-if="songTitleWidth > minWidth"
            >
              {{ `${Math.trunc(song.length / 60)} min` }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else ref="songtitle"></div>
  </div>
</template>

<script>
import { ref, toRefs } from "@vue/reactivity";
import { onMounted, onUnmounted } from "@vue/runtime-core";

import audio from "@/composables/playAudio.js";
import getQueue from "@/composables/getQueue.js";
import perks from "@/composables/perks.js";

export default {
  props: ["songs"],
  setup(props) {
    const song_list = toRefs(props).songs;
    const songtitle = ref(null);
    const songTitleWidth = ref(null);

    const minWidth = ref(300);
    const putCommas = perks.putCommas;

    const updateQueue = async (song, type, id) => {
      if (perks.queue.value[0]._id.$oid !== song_list.value[0]._id.$oid) {
        const queue = await getQueue(type, id);
        localStorage.setItem("queue", JSON.stringify(queue));
        perks.queue.value = queue;
      }

      perks.current.value = song;
      localStorage.setItem("current", JSON.stringify(song));
    };

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

    const playAudio = audio.playAudio;

    return {
      songtitle,
      songTitleWidth,
      minWidth,
      playAudio,
      updateQueue,
      putCommas,
    };
  },
};
</script>

<style lang="scss">
.table {
  width: 100%;
  height: 100%;
  background-color: rgba(56, 56, 56, 0.363);
  overflow-y: auto;

  &::-webkit-scrollbar {
    display: none;
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
  outline: none;
  border: none;
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
  font-weight: lighter;
  margin-right: 0.5rem;
}

.folder .table table {
  border-collapse: collapse;
  text-transform: capitalize;
  position: relative;
  margin: 1rem;

  tbody tr {
    cursor: pointer;
    transition: all 0.1s ease;

    &:hover {
      & {
        background-color: rgb(5, 80, 150);
      }
    }
  }
}
</style>