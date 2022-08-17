<template>
  <div
    class="loaderx"
    :class="{ loader: loader.loading, not_loader: !loader.loading }"
    @click="modal.showSearchModal"
  >
    <div v-if="!loader.loading">🦋</div>
  </div>
</template>

<script setup lang="ts">
import useLoaderStore from "@/stores/loader";
import useModalStore from "@/stores/modal";

const loader = useLoaderStore();
const modal = useModalStore();
</script>

<style lang="scss">
.loaderx {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  user-select: none;
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
