<template>
  <div class="r-home">
   <Recommendations />
  </div>
</template>

<style lang="scss">
.r-home {
  height: calc(100% - 1rem);
  // padding: 0 $small $small 0;
}
</style>

<script setup>
import Recommendations from '../Recommendation.vue';
</script>