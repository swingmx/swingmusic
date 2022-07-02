<template>
  <div class="folder">
    <div class="table rounded" v-if="tracks.length">
      <div class="songlist">
        <SongItem
          v-for="track in getTracks()"
          :key="track.trackid"
          :song="track"
          :index="track.index"
          @updateQueue="updateQueue"
          :isPlaying="queue.playing"
          :isCurrent="queue.current.trackid == track.trackid"
        />
      </div>
    </div>
    <div v-else-if="tracks.length === 0">
      <div class="no-results">
        <div class="text">No tracks here</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";

import SongItem from "../shared/SongItem.vue";

import useQStore from "../../stores/queue";
import { Track } from "../../interfaces";

const queue = useQStore();

const props = defineProps<{
  tracks: Track[];
  path?: string;
  pname?: string;
  playlistid?: string;
  on_album_page?: boolean;
}>();

let route = useRoute().name;

/**
 * Plays a clicked track and updates the queue
 *
 * @param track Track object
 */
function updateQueue(track: Track) {
  switch (route) {
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

function getTracks() {
  if (props.on_album_page) {
    let tracks = props.tracks.map((track, index) => {
      track.index = track.tracknumber;
      return track;
    });

    return tracks;
  }

  let tracks = props.tracks.map((track, index) => {
    track.index = index + 1;
    return track;
  });

  return tracks;
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
  overflow-y: hidden;

  .current {
    a {
      color: inherit;
    }
    color: $red;
  }

  .current:hover {
    * {
      color: rgb(255, 255, 255);
    }
  }

  .songlist {
    scrollbar-width: none;
    &::-webkit-scrollbar {
      display: none;
    }
    .context-on {
      background-color: $gray4;
      color: $white !important;
    }
  }
}
</style>
