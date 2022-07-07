<template>
  <div class="bottom-content">
    <FeaturedArtists :artists="artists" />
    <div v-if="bio">
      <div class="separator" id="av-sep"></div>
      <AlbumBio :bio="bio" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Artist } from "@/interfaces";
import FeaturedArtists from "@/components/PlaylistView/FeaturedArtists.vue";
import AlbumBio from "@/components/AlbumView/AlbumBio.vue";

defineProps<{
  artists: Artist[];
  bio: string | null;
}>();
</script>

<style lang="scss"></style>
