<template>
  <div class="folder">
    <div class="table rounded" v-if="tracks.length">
      <div class="header" v-if="disc && !album.info.is_single">
        <div class="disc-number">Disc {{ disc }}</div>
      </div>
      <div class="songlist">
        <SongItem
          v-for="track in getTrackList()"
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
    <div class="copyright" v-if="copyright">
      {{ copyright() }}
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
import useAlbumStore from "@/stores/pages/album";

const queue = useQStore();
const album = useAlbumStore();

const props = defineProps<{
  tracks: Track[];
  path?: string;
  pname?: string;
  playlistid?: string;
  on_album_page?: boolean;
  disc?: string | number;
  copyright?: () => string;
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
      const tindex = album.tracks.findIndex((t) => t.trackid === track.trackid);

      queue.playFromAlbum(
        track.album,
        track.albumartist,
        track.albumhash,
        album.tracks
      );
      queue.play(tindex);
      break;
    case "PlaylistView":
      queue.playFromPlaylist(props.pname, props.playlistid, props.tracks);
      queue.play(index);
      break;
  }
}

/**
 * Used to show track numbers as indexes in the album page.
 */
function getTrackList() {
  if (props.on_album_page) {
    let tracks = props.tracks.map((track) => {
      track.index = track.tracknumber;
      return track;
    });

    return tracks;
  }

  const tracks = props.tracks.map((track, index) => {
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

.copyright {
  font-size: 0.8rem;
  margin-top: 1rem;
  text-align: center;
  opacity: 0.5;
}

.table {
  height: 100%;
  overflow-y: hidden;
  background-color: $gray5;
  padding: $small 0;

  .header {
    margin: $small;

    .disc-number {
      font-size: small;
      font-weight: bold;
      margin: $small 1.5rem;
      color: $gray1;
    }
  }

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

    .contexton {
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
