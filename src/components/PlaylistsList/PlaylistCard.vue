<template>
  <router-link
    :to="{ name: 'PlaylistView', params: { pid: props.playlist.playlistid } }"
    :playlist="props.playlist"
    class="p-card rounded noscroll"
  >
    <img :src="imguri + props.playlist.thumb" />
    <div class="overlay rounded pad-lg">
      <div class="p-name ellip">{{ playlist.name }}</div>
      <div class="p-count">
        {{ playlist.count + ` ${playlist.count == 1 ? "Track" : "Tracks"}` }}
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import play from "@/composables/usePlayFrom";
import { paths } from "../../config";
import { Playlist } from "../../interfaces";

const imguri = paths.images.playlist;

const props = defineProps<{
  playlist: Playlist;
}>();
</script>

<style lang="scss">
.p-card {
  transition: all 0.25s ease;
  position: relative;
  background-color: $playlist-card-bg;
  height: 10rem;

  img {
    width: 100%;
    height: 100%;
    aspect-ratio: 1/1.2;
    object-fit: cover;
    transition: all 0.25s ease;
  }

  .overlay {
    position: absolute;
    top: 0;
    background-image: linear-gradient(
      to top,
      rgba(0, 0, 0, 0.55),
      transparent 60%
    );
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    transition: all 0.25s ease;

    .p-count {
      opacity: 0.75;
      font-size: 0.75rem;
    }
  }

  &:hover {
    img {
      transform: scale(1.1);
    }
  }

  .bottom {
    margin-top: $smaller;

    .name {
      font-weight: 900;
    }

    .count {
      font-size: $medium;
      opacity: 0.5;
    }
  }
}
</style>
