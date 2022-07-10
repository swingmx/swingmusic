<template>
  <div class="folder">
    <div class="table rounded" v-if="tracks.length">
      <div class="songlist">
        <SongItem
          v-for="track in getTracks()"
          :key="track.trackid"
          :track="track"
          :index="track.index"
          @updateQueue="updateQueue"
          :isPlaying="queue.playing"
          :isCurrent="queue.currentid == track.trackid"
          :isHighlighted="highlightid == track.uniq_hash"
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
import { onBeforeRouteUpdate, useRoute } from "vue-router";

import SongItem from "../shared/SongItem.vue";

import { focusElem } from "@/composables/perks";
import { onMounted, onUpdated, ref } from "vue";
import { Track } from "@/interfaces";
import useQStore from "@/stores/queue";

const queue = useQStore();

const props = defineProps<{
  tracks: Track[];
  path?: string;
  pname?: string;
  playlistid?: string;
  on_album_page?: boolean;
}>();

const route = useRoute();
const routename = route.name as string;
const highlightid = ref(route.query.highlight as string);

function highlightTrack(t_hash: string) {
  focusElem(`track-${t_hash}`, 500, "center");
}

onBeforeRouteUpdate(async (to, from) => {
  const h_hash = to.query.highlight as string;
  highlightid.value = h_hash as string;

  if (h_hash) {
    highlightTrack(h_hash);
  }
});

onUpdated(() => {
  if (highlightid.value) {
    highlightTrack(highlightid.value);
  }
});

onMounted(() => {
  if (highlightid.value) {
    highlightTrack(highlightid.value);
  }
});
/**
 * Plays a clicked track and updates the queue
 *
 * @param track Track object
 */
function updateQueue(track: Track) {
  const index = props.tracks.findIndex(
    (t: Track) => t.trackid === track.trackid
  );

  switch (routename) {
    case "FolderView":
      queue.playFromFolder(props.path, props.tracks);
      queue.play(index);
      break;
    case "AlbumView":
      queue.playFromAlbum(track.album, track.albumartist, props.tracks);
      queue.play(index);
      break;
    case "PlaylistView":
      queue.playFromPlaylist(props.pname, props.playlistid, props.tracks);
      queue.play(index);
      break;
  }
}

function getTracks() {
  if (props.on_album_page) {
    let tracks = props.tracks.map((track) => {
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

    .highlighted {
      color: $white !important;
      animation: blinker 1.5s ease 1s;
    }

    @keyframes blinker {
      25% {
        background-color: $gray4;
      }

      50% {
        background-color: transparent;
      }

      75% {
        background-color: $gray4;
      }
    }
  }
}
</style>
