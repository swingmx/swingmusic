<template>
  <router-link
    :to="{ name: 'PlaylistView', params: { pid: props.playlist.playlistid } }"
    :playlist="props.playlist"
    class="p-card rounded bg-primary"
  >
    <img :src="imguri + props.playlist.thumb" class="rounded" />
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
import { paths } from "../../config";
import { Playlist } from "../../interfaces";

const imguri = paths.images.playlist;

const props = defineProps<{
  playlist: Playlist;
}>();
</script>

<style lang="scss">
.p-card {
  width: 100%;
  padding: 1rem;
  transition: all 0.25s ease;
  position: relative;

  img {
    width: 100%;
    aspect-ratio: 1;
    object-fit: cover;
  }

  &:hover {
    background-color: $darkestblue;
  }

  .bottom {
    margin-top: $smaller;
    display: grid;
    justify-items: center;

    .name {
      font-weight: 900;
    }

    .count {
      font-size: $medium;
      opacity: .5;
    }
  }
}
</style>
