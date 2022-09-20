<template>
  <div v-tooltip style="width: auto">
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
</script>
