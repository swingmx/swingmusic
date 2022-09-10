<template>
  <div class="songlist rounded">
    <div v-if="tracks.length">
      <SongList
        :tracks="tracks"
        :pname="name"
        :playlistid="playlistid"
        @playFromPage="playFromPlaylistPage"
      />
    </div>
    <div v-else-if="tracks.length === 0 && count > 0">
      <div class="no-results">
        <div class="text">We can't find your music 🦋</div>
      </div>
    </div>
    <div v-else-if="tracks.length === 0 && count == 0">
      <div class="no-results">
        <div class="text">Nothing here</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import useQueueStore from "@/stores/queue";
import usePlaylistStore from "@/stores/pages/playlist";

import SongList from "@/components/FolderView/SongList.vue";
import { Track } from "@/interfaces";
import { onUpdated } from "vue";

const props = defineProps<{
  tracks: Track[];
  count: number;
  name: string;
  playlistid: string;
}>();

const queue = useQueueStore();
const playlist = usePlaylistStore();

function playFromPlaylistPage(index: number) {
  const { name, playlistid } = playlist.info;
  queue.playFromPlaylist(name, playlistid, playlist.allTracks);
  queue.play(index);
}
</script>
