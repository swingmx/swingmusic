<template>
  <div
    class="table rounded border"
    v-if="tracks.length"
    ref="tracklistElem"
    :class="{
      isSmall: isSmall,
      isMedium: isMedium,
    }"
  >
    <div class="header">
      <div class="disc-number" v-if="disc">Disc {{ disc }}</div>
      <div class="disc-number" v-if="$route.name === Routes.folder">
        In this folder
      </div>
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
        :isHighlighted="($route.query.highlight as string) == track.hash"
      />
    </div>
    <div class="copyright" v-if="copyright && copyright()">
      {{ copyright() }}
    </div>
  </div>
  <div v-else-if="tracks.length === 0">
    <div class="no-results">
      <div class="text">No tracks here</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUpdated, ref } from "vue";
import { onBeforeRouteUpdate, useRoute } from "vue-router";
import { useElementSize } from "@vueuse/core";

import SongItem from "../shared/SongItem.vue";

import { Routes } from "@/composables/enums";
import { Track } from "@/interfaces";
import useAlbumStore from "@/stores/pages/album";
import useQStore from "@/stores/queue";
import { focusElem } from "@/utils";
import { computed } from "@vue/reactivity";

const queue = useQStore();
const album = useAlbumStore();

const props = defineProps<{
  tracks: Track[];
  path?: string;
  pname?: string;
  playlistid?: string;
  on_album_page?: boolean;
  disc?: string | number;
  copyright?: (() => string) | null;
}>();

const route = useRoute();
const routename = route.name as string;
const highlightid = ref(route.query.highlight as string | null);

const tracklistElem = ref<HTMLElement | null>(null);
const { width, height } = useElementSize(tracklistElem);

const brk = {
  sm: 500,
  md: 800,
};

const isSmall = computed(() => width.value < brk.sm);
const isMedium = computed(() => width.value > brk.sm && width.value < brk.md);

function highlightTrack(t_hash: string) {
  focusElem(`track-${t_hash}`, 500, "center");
}

function resetHighlight() {
  setTimeout(() => {
    highlightid.value = null;
  }, 1000);
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
    resetHighlight();
  }
});

onMounted(() => {
  if (highlightid.value) {
    highlightTrack(highlightid.value);
    resetHighlight();
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
    case Routes.folder:
      queue.playFromFolder(props.path || "", props.tracks);
      queue.play(index);
      break;
    case Routes.album:
      const tindex = album.tracks.findIndex((t) => t.trackid === track.trackid);

      queue.playFromAlbum(
        track.album || "",
        track.albumartist || "",
        track.albumhash || "",
        album.tracks
      );
      queue.play(tindex);
      break;
    case Routes.playlist:
      queue.playFromPlaylist(
        props.pname || "",
        props.playlistid || "",
        props.tracks
      );
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

.table.isSmall {
  .songlist-item {
    grid-template-columns: 1.5rem 1.5fr 2rem 2.5rem;
  }

  .song-artists,
  .song-album {
    display: none !important;
  }

  .isSmallArtists {
    display: unset !important;
    font-size: small;
    color: $white;
    opacity: 0.67;
  }
}

.table.isMedium {
  .songlist-item {
    grid-template-columns: 1.5rem 1.5fr 1fr 2rem 2.5rem;
  }

  .song-album {
    display: none !important;
  }
}
</style>
