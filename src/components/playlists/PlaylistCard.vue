<template>
  <router-link
    :to="{ name: 'PlaylistView', params: { pid: props.playlist.playlistid } }"
    :playlist="props.playlist"
    class="p-card rounded"
  >
    <div
      class="image rounded"
      :style="{
        backgroundImage: `url(${props.playlist.image})`,
      }"
    ></div>
    <div class="bottom">
      <div class="name ellip">{{ props.playlist.name }}</div>
      <div class="count">
        <span v-if="props.playlist.count == 0">No Tracks</span>
        <span v-else-if="props.playlist.count == 1"
          >{{ props.playlist.count }} Track</span
        >
        <span v-else>{{ props.playlist.count }} Tracks</span>
      </div>
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
    height: 11rem;
    transition: all 0.2s ease;
  }

  .bottom {
    margin-top: $small;

    .name {
      text-transform: capitalize;
    }

    .count {
      font-size: $medium;
      color: $gray1;
    }
  }
}
</style>
