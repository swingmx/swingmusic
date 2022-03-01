<template>
  <div class="loaderx" :class="{ loader: loading, not_loader: !loading }">
    <div v-if="!loading">😹</div>
  </div>
</template>

<script setup>
import state from "@/composables/state.js";

const loading = state.loading
</script>

<style lang="scss">
.loaderx {
  position: absolute;
  top: 0.65rem;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
}

.loader {
  border: dotted $blue;
  animation: spin 0.25s linear infinite;

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
}

.not_loader {
  display: grid;
  place-items: center;
}
</style>
