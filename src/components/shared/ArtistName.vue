<template>
  <div
    v-tooltip
    style="width: fit-content"
    class="ellip"
    :style="{
      fontSize: small ? '0.85rem' : smaller ? 'small' : '',
    }"
  >
    <div v-if="artists === null || artists.length === 0">
      <span>{{ albumartists }}</span>
    </div>
    <div v-else>
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
  albumartists: string | null;
  small?: boolean;
  smaller?: boolean;
}>();
</script>
