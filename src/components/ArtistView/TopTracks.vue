<template>
  <div class="artist-top-tracks">
    <h3 class="section-title">
      {{ title }}
      <span class="see-all">

        <RouterLink :to="route">SEE ALL</RouterLink>
      </span>
    </h3>
    <div class="tracks" :class="{ isSmall, isMedium }">
      <SongItem
        v-for="(song, index) in tracks"
        :track="song"
        :index="index + 1"
        @playThis="playHandler(index)"
      />
    </div>
    <div class="error" v-if="!tracks.length">No tracks</div>
  </div>
</template>

<script setup lang="ts">
import SongItem from "../shared/SongItem.vue";
import { Track } from "@/interfaces";
import { isMedium, isSmall } from "@/stores/content-width";

defineProps<{
  tracks: Track[];
  route: string;
  title: string;
  playHandler: (index: number) => void;
}>();
</script>

<style lang="scss">
.artist-top-tracks {
  margin-top: 2rem;

  .section-title {
    margin-left: 0;
  }

  .error {
    padding-left: 1rem;
    color: $red;
  }

  h3 {
    display: flex;
    justify-content: space-between;
  }

  .see-all {
    font-size: $medium;

    a:hover {
      text-decoration: underline;
      cursor: pointer !important;
    }
  }
}
</style>
