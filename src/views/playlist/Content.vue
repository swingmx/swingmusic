<template>
  <div class="songlist rounded">
    <div v-if="tracks.length">
      <SongList :tracks="tracks" :pname="name" :playlistid="playlistid" />
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
import SongList from "@/components/FolderView/SongList.vue";
import { Track } from "@/interfaces";

defineProps<{
  tracks: Track[];
  count: number;
  name: string;
  playlistid: string;
}>();
</script>
