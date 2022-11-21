<template>
  <router-link
    :to="{ name: 'PlaylistView', params: { pid: playlist.id } }"
    class="p-card rounded no-scroll"
  >
    <img
      :src="imguri + playlist.thumb"
      class="rounded"
      :class="{ border: !playlist.thumb }"
    />
    <div class="overlay rounded">
      <div class="p-name ellip">{{ playlist.name }}</div>
      <div class="p-count">
        {{ playlist.count + ` ${playlist.count === 1 ? "Track" : "Tracks"}` }}
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
  background-color: #2c2c2e45;
  display: grid;
  grid-template-rows: 1fr max-content;
  padding: 1rem;
  gap: $small;

  &:hover {
    transition: all .25s ease;
    background-color: $gray3;
    background-blend-mode: screen;
  }

  img {
    width: 100%;
    aspect-ratio: 1;
    object-fit: cover;
    transition: all 0.5s ease;
  }
  .overlay {
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
    .p-name {
      text-decoration: underline;
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
