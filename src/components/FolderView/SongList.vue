<template>
  <div
    class="table border rounded"
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
        v-for="(track, index) in getTrackList()"
        :key="track.trackid"
        :track="track"
        :index="track.index !== undefined ? track.index + 1 : index + 1"
        @updateQueue="updateQueue(track.index)"
        :isPlaying="queue.playing"
        :isCurrent="queue.currentid == track.trackid"
      />
    </div>
    <div class="copyright" v-if="copyright && copyright">
      {{ copyright }}
    </div>
  </div>
  <div v-else-if="tracks.length === 0">
    <div class="no-results">
      <div class="text">No tracks here</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onUpdated, ref } from "vue";
import { useElementSize } from "@vueuse/core";
import { computed } from "@vue/reactivity";

import SongItem from "../shared/SongItem.vue";

import { Routes } from "@/composables/enums";
import { Track } from "@/interfaces";
import useQStore from "@/stores/queue";

const queue = useQStore();

const props = defineProps<{
  tracks: Track[];
  path?: string;
  pname?: string;
  playlistid?: string;
  on_album_page?: boolean;
  disc?: string | number;
  copyright?: string | null;
}>();

// onUpdated(() => {
//   console.log(props.tracks[1].index);
// });

const emit = defineEmits<{
  (e: "playFromPage", index: number): void;
}>();

const tracklistElem = ref<HTMLElement | null>(null);
const { width } = useElementSize(tracklistElem);

const brk = {
  sm: 500,
  md: 800,
};

const isSmall = computed(() => width.value < brk.sm);
const isMedium = computed(() => width.value > brk.sm && width.value < brk.md);

function updateQueue(index: number) {
  emit("playFromPage", index);
}

/**
 * Used to show handle track indexes.
 */
function getTrackList() {
  if (props.on_album_page) {
    const tracks = props.tracks.map((track) => {
      track.index = track.tracknumber;
      return track;
    });

    return tracks;
  }

  return props.tracks;
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
