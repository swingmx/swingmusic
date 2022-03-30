<template>
  <div class="info">
    <div class="desc">
      <div>
        <div class="title ellip">{{ props.track.title }}</div>
        <div class="separator no-border"></div>
        <div class="artists ellip" v-if="props.track.artists[0] !== ''">
          <span
            v-for="artist in putCommas(props.track.artists)"
            :key="artist"
            >{{ artist }}</span
          >
        </div>
        <div class="artists" v-else>
          <span>{{ props.track.albumartist }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import perks from "../../composables/perks";
import { Track } from "../../interfaces";
const putCommas = perks.putCommas;

const props = defineProps<{
  track: Track;
}>();
</script>
