<template>
  <div class="loader" v-if="loading"></div>
</template>

<script>
import state from "@/composables/state.js";
export default {
  setup() {
    return {
      loading: state.loading,
    };
  },
};
</script>

<style lang="scss">
.loader {
  position: absolute;
  right: 0.65rem;
  top: 0.65rem;
  width: 1.5rem;
  height: 1.5rem;
  border: dotted $blue;
  border-radius: 50%;
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
</style>