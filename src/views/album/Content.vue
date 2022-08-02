<template>
  <div class="album-tracks rounded">
    <div v-for="(disc, key) in discs" class="album-disc">
      <SongList :key="key" :tracks="disc" :on_album_page="true" :disc="key" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Track } from "@/interfaces";
import SongList from "@/components/FolderView/SongList.vue";

defineProps<{
  discs: {
    [key: string]: Track[];
  };
}>();
</script>

<style lang="scss">
.album-tracks {
  display: grid;
  gap: 1rem;
}
</style>
