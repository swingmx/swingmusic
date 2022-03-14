<template>
  <div class="folder">
    <div class="table rounded" v-if="props.songs.length">
      <div class="thead">
        <div class="index"></div>
        <div class="track-header">Track</div>
        <div class="artists-header">Artist</div>
        <div class="album-header">Album</div>
        <div class="duration-header">Duration</div>
      </div>
      <div>
        <SongItem
          v-for="(song, index) in props.songs"
          :key="song"
          :song="song"
          :index="index + 1"
          @updateQueue="updateQueue"
          @loadAlbum="loadAlbum"
        />
      </div>
    </div>
    <div v-else-if="props.songs.length === 0 && search_query">
      <div class="no-results">
        <div class="text">Nothing down here 😑</div>
      </div>
    </div>
    <div v-else ref="songtitle"></div>
  </div>
</template>

<script setup>
import { onMounted } from "@vue/runtime-core";
import { useRoute } from "vue-router";

import SongItem from "../shared/SongItem.vue";

import routeLoader from "@/composables/routeLoader.js";
import perks from "@/composables/perks.js";
import state from "@/composables/state.js";

const props = defineProps({
  songs: {
    type: Array,
    required: true,
  },
});

let route;

const search_query = state.search_query;

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

function loadAlbum(title, albumartist) {
  routeLoader.toAlbum(title, albumartist);
}
</script>

<style lang="scss">
.no-results {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 1rem;
}

.table {
  width: 100%;
  height: 100%;
  overflow-y: auto;

  .current {
    color: $red;
  }

  .current:hover {
    * {
      color: rgb(255, 255, 255);
    }
  }

  .thead {
    display: grid;
    grid-template-columns: 1.5rem 1.5fr 1fr 1.5fr 0.25fr;
    height: 2.5rem;
    align-items: center;
    text-transform: uppercase;
    font-weight: bold;
    color: $gray1;
    gap: $small;

    @include tablet-landscape {
      grid-template-columns: 1.5rem 1.5fr 1fr 1.5fr;
    }

    @include tablet-portrait {
      grid-template-columns: 1.5rem 1.5fr 1fr;
    }

    @include phone-only {
      display: none;
    }

    .duration-header {
      @include tablet-landscape {
        display: none;
      }

      width: 6rem;
    }

    .album-header {
      @include tablet-portrait {
        display: none;
      }
    }

    &::-webkit-scrollbar {
      display: none;
    }
  }
}
</style>
