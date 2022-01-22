<template>
  <div class="folder">
    <div class="table rounded" v-if="songs.length">
      <table>
        <thead>
          <tr>
            <th class="track-header">Track</th>
            <th class="artists-header">Artist</th>
            <th class="album-header">Album</th>
            <th class="duration-header">Duration</th>
          </tr>
        </thead>
        <tbody>
          <SongItem
            v-for="song in songs"
            :key="song"
            :song="song"
            @updateQueue="updateQueue"
            @loadAlbum="loadAlbum"
          />
        </tbody>
      </table>
    </div>
    <div v-else-if="songs.length === 0 && search_query">
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
import { onMounted } from "@vue/runtime-core";

import SongItem from "../shared/SongItem.vue";
import routeLoader from "@/composables/routeLoader.js";
import perks from "@/composables/perks.js";
import state from "@/composables/state.js";
import { useRoute } from "vue-router";

export default {
  props: ["songs"],
  components: {
    SongItem,
  },
  setup() {
    let route;

    const current = ref(perks.current);
    const search_query = ref(state.search_query);

    onMounted(() => {
      route = useRoute().name;
    });

    function updateQueue(song) {
      let type;

      switch (route) {
        // check which route the play request come from
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
      routeLoader.toAlbum(title, album_artist);
    }

    return {
      updateQueue,
      loadAlbum,
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

table {
  border-collapse: collapse;
  text-transform: capitalize;
  width: 100%;
  table-layout: fixed;

  @include phone-only {
    border-collapse: separate;
    border-spacing: 0 $small;
  }

  thead {
    height: 2rem;
    text-transform: uppercase;

    @include phone-only {
      display: none;
    }

    th {
      text-align: left;
      padding-left: $small;
    }

    th.duration-header {
      @include tablet-landscape {
        display: none;
      }

      width: 5rem;
    }

    th.album-header {
      @include tablet-portrait {
        display: none;
      }
    }
  }
}
</style>