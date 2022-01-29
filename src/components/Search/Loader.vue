<template>
  <div class="loaderx" :class="{ loader: loading, not_loader: !loading }">
    <div class="content" v-if="!loading">/</div>
  </div>
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
.loaderx {
  position: absolute;
  left: 0.65rem;
  top: 0.65rem;
  width: 1.5rem;
  height: 1.5rem;
}

.loader {
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

.not_loader {
  border: solid 1px;
  border-radius: 50%;
  background-image: url("");
}
</style>
