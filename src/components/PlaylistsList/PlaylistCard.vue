<template>
  <router-link
    :to="{ name: 'PlaylistView', params: { pid: props.playlist.playlistid } }"
    :playlist="props.playlist"
    class="p-card rounded bg-primary"
  >
    <div
      class="image p-image rounded shadow-sm"
      :style="{
        backgroundImage: `url(${imguri + props.playlist.thumb})`,
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

  .p-image {
    min-width: 100%;
    transition: all 0.2s ease;
    background-color: $gray4;
    aspect-ratio: 1;
  }

  .drop {
    position: absolute;
    bottom: 4rem;
    right: 1.25rem;
    opacity: 0;
    transition: all 0.25s ease-in-out;
    display: none;

    .drop-btn {
      background-color: $gray3;
    }
  }

  .pbtn {
    display: none;
    position: absolute;
    bottom: 4.5rem;
    left: 1.25rem;
    transition: all 0.25s ease-in-out;
    z-index: 10;
  }

  &:hover {
    background-color: $gray2;

    .drop {
      transition-delay: 0.75s;
      opacity: 1;
      transform: translate(0, -0.5rem);
    }
  }

  .bottom {
    margin-top: 1rem;

    .name {
      font-weight: 900;
    }

    .count {
      font-size: $medium;
      color: $gray1;
    }
  }
}
</style>
