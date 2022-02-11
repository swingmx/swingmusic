<template>
  <div class="l_">
    <div
      class="l-image image border rounded"
      :style="{
        backgroundImage: `url(&quot;${current.image}&quot;)`,
      }"
    ></div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import state from "../../composables/state";

const current = ref(state.current);
</script>
<style lang="scss">
.l_ {
  padding: $small;
  
  .l-image {
    height: 14rem;
    width: 14rem;
  }
}
</style>
