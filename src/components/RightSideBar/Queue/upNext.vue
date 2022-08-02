<template>
  <div class="main-item bg-black" @click="playNext">
    <div class="h">Up Next</div>
    <div class="itemx shadow">
      <div
        class="album-art image"
        :style="{
          backgroundImage: `url(&quot;${imguri + next.image}&quot;)`,
        }"
      ></div>
      <div class="tags">
        <p class="title ellip">{{ next.title }}</p>
        <hr />
        <p class="artist ellip">
          <span v-for="artist in putCommas(next.artists)" :key="artist">{{
            artist
          }}</span>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { putCommas } from "@/composables/perks";
import { paths } from "@/config";
import { Track } from "@/interfaces";

const imguri = paths.images.thumb;
defineProps<{
  next: Track;
  playNext: () => void;
}>();
</script>

<style lang="scss">
.main-item {
  border-radius: 0.5rem;
  position: relative;

  &:hover {
    background-color: $accent;

    .h {
      background-color: $black;
    }
  }

  .h {
    position: absolute;
    right: $small;
    bottom: $small;
    font-size: 0.9rem;
    background-color: $accent;
    padding: $smaller;
    border-radius: 0.25rem;
  }

  .itemx {
    display: flex;
    align-items: center;
    border-radius: 0.5rem;
    padding: 0.75rem;
    cursor: pointer;
  }

  .album-art {
    width: 4.5rem;
    height: 4.5rem;
    background-image: url(../../assets/images/null.webp);
    margin: 0 0.5rem 0 0;
    border-radius: 0.5rem;
  }

  .tags {
    hr {
      border: none;
      margin: 0.3rem;
    }
    .title {
      width: 20rem;
      margin: 0;
    }
    .artist {
      width: 20rem;
      margin: 0;
      font-size: small;
    }
  }
}
</style>
