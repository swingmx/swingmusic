<template>
  <div class="info">
    <div
      class="image art"
      :style="{
        backgroundImage: `url(&quot;${track.image}&quot;)`,
      }"
    ></div>
    <div class="desc">
      <div>
        <div class="title ellip">{{ track.title }}</div>
        <div class="separator no-border"></div>
        <div class="artists ellip" v-if="track.artists[0] != ''">
          <span v-for="artist in putCommas(track.artists)" :key="artist">{{
            artist
          }}</span>
        </div>
        <div class="artists" v-else>
          <span>{{ track.album_artist }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import perks from "../../composables/perks";

const track = ref(perks.current);

const putCommas = perks.putCommas;
</script>
