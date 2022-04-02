<template>
  <router-link
    :to="{ name: 'PlaylistView', params: { pid: props.playlist.playlistid } }"
    :playlist="props.playlist"
    class="p-card rounded shadow-sm"
  >
    <div class="image rounded"></div>
    <div class="bottom">
      <div class="name ellip">{{ props.playlist.name }}</div>
      <div class="count">{{ props.playlist.count }} Tracks</div>
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
  background: $gray;
  padding: $small;
  transition: all 0.2s ease;

  &:hover {
    background-color: $accent;
    .bottom > .count {
      color: $white;
    }
  }

  .image {
    min-width: 100%;
    height: 10rem;
    background-image: url("../../assets/images/eggs.jpg");
    background-size: auto 10rem;
    transition: all 0.2s ease;
  }

  .bottom {
    margin-top: $small;

    .name {
      text-transform: capitalize;
    }

    .count {
      font-size: $medium;
      color: $indigo;
    }
  }
}
</style>
