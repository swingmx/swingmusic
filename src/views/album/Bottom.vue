<template>
  <div class="bottom-content">
    <FeaturedArtists :artists="artists" />

    <AlbumBio :bio="bio" :images="{ album: image, artist: artists[0].image }" />
  </div>
</template>

<script setup lang="ts">
import { Artist } from "@/interfaces";
import FeaturedArtists from "@/components/PlaylistView/FeaturedArtists.vue";
import AlbumBio from "@/components/AlbumView/AlbumBio.vue";

defineProps<{
  artists: Artist[];
  bio: string | null;
  image: string;
}>();
</script>

<style lang="scss"></style>
