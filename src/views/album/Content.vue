<template>
  <div class="songs rounded">
    <SongList :tracks="tracks" :on_album_page="true" />
  </div>
</template>

<script setup lang="ts">
import { Track } from "@/interfaces";
import SongList from "@/components/FolderView/SongList.vue";

defineProps<{
  tracks: Track[];
}>();
</script>
