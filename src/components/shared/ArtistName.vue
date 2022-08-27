<template>
  <div class="ellip" v-if="artists[0] !== ''">
    <span v-for="artist in putCommas(artists)" :key="artist">{{ artist }}</span>
  </div>
  <div class="ellip" v-else>
    <span>{{ albumartist }}</span>
  </div>
</template>

<script setup lang="ts">
import { putCommas } from "@/utils";

defineProps<{
  artists: string[];
  albumartist: string | undefined;
}>();
</script>
