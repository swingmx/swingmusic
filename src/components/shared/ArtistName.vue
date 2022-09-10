<template>
  <div v-tooltip="returnArtists()" style="width: auto">
    <div
      class="ellip"
      v-if="artists.length === 0 || (artists[0] === '' && artists.length === 1)"
    >
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
  artists: string[];
  albumartist: string | undefined;
}>();

function returnArtists() {
  if (props.artists[0] !== "" && props.artists.length > 1) {
    return props.artists.join(", ");
  } else {
    return props.albumartist;
  }
}
</script>
