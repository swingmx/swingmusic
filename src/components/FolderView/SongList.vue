<template>
  <div class="folder">
    <div class="table rounded" v-if="props.tracks.length">
      <div class="thead">
        <div class="index"></div>
        <div class="track-header">Track</div>
        <div class="artists-header">Artist</div>
        <div class="album-header">Album</div>
        <div class="duration-header">Duration</div>
      </div>
      <div class="songlist">
        <SongItem
          v-for="(song, index) in props.tracks"
          :key="song.trackid"
          :song="song"
          :index="index + 1"
          @updateQueue="updateQueue"
          :isPlaying="queue.playing"
          :isCurrent="queue.current.trackid == song.trackid"
        />
      </div>
    </div>
    <div v-else-if="props.tracks.length === 0 && search_query">
      <div class="no-results">
        <div class="text">Nothing down here 😑</div>
      </div>
    </div>
    <div v-else ref="songtitle"></div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";

import SongItem from "../shared/SongItem.vue";

import state from "../../composables/state";
import useQStore from "../../stores/queue";
import { Track } from "../../interfaces";

const queue = useQStore();

const props = defineProps<{
  tracks: Track[];
  path?: string;
  pname?: string;
  playlistid?: string;
}>();

let route = useRoute().name;
const search_query = state.search_query;

function updateQueue(track: Track) {
  switch (route) {
    // check which route the play request come from
    case "FolderView":
      queue.playFromFolder(props.path, props.tracks);
      queue.play(track);
      break;
    case "AlbumView":
      queue.playFromAlbum(track.album, track.albumartist, props.tracks);
      queue.play(track);
      break;
    case "PlaylistView":
      queue.playFromPlaylist(props.pname, props.playlistid, props.tracks);
      queue.play(track);
      break;
  }
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

  .songlist {
    .context-on {
      background-color: $gray4;
      color: $white !important;
    }
  }
}
</style>
