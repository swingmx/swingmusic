<template>
  <div class="r-home rounded border">
   <NowPlaying />
   <Recommendations />
  </div>
</template>

<style lang="scss">
.r-home {
  height: 100%;
  width: 31rem;
  background-color: $card-dark;
  padding: $small;
}
</style>

<script setup>
import NowPlaying from '../NowPlaying.vue';
import Recommendations from '../Recommendation.vue';
</script>