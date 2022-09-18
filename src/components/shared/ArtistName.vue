<template>
  <div v-tooltip="returnArtists()" style="width: auto">
    <div class="ellip" v-if="artists === null || artists.length === 0">
      <span>{{ albumartist }}</span>
    </div>
    <div class="ellip" v-else>
      <span v-for="artist in putCommas(artists)" :key="artist">{{
        artist
      }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { putCommas } from "@/utils";

const props = defineProps<{
  artists: string[] | null;
  albumartist: string | undefined;
}>();

function returnArtists() {
  if (props.artists === null || props.artists.length === 0)
    return props.albumartist;

  return props.artists.join(", ");
}
</script>
