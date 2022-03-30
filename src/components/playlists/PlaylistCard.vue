<template>
  <router-link
    :to="{ name: 'PlaylistView', params: { pid: props.playlist.playlistid } }"
    :playlist="props.playlist"
    class="p-card rounded shadow-sm"
  >
    <div class="image rounded"></div>
    <div class="bottom">
      <div class="name ellip">{{ props.playlist.name }}</div>
      <div class="count">N Tracks</div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { Playlist } from "../../interfaces";

const props = defineProps<{
  playlist: Playlist;
}>();
</script>

<style lang="scss">
.p-card {
  width: 100%;
  background-color: $gray;
  padding: $small;

  .image {
    min-width: 100%;
    height: 10rem;
    background-image: url("../../assets/images/eggs.jpg");
  }

  .bottom {
    margin-top: $small;

    .count {
      font-size: $medium;
      color: $red;
    }
  }
}
</style>
