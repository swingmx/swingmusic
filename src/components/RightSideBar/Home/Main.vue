<template>
  <div class="r-home">
   <NowPlaying />
   <Recommendations />
  </div>
</template>

<style lang="scss">
.r-home {
  height: 100%;
  width: 31rem;
}
</style>

<script setup>
import NowPlaying from '../NowPlaying.vue';
import Recommendations from '../Recommendation.vue';
</script>