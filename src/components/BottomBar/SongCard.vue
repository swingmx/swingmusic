<template>
  <div class="info">
    <div
      v-if="props.collapsed"
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
          <span>{{ track.albumartist }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import perks from "../../composables/perks";
import state from "../../composables/state";

const track = state.current;
const props = defineProps({
  collapsed: {
    type: Boolean,
    default: false,
  },
});
const putCommas = perks.putCommas;
</script>
