<template>
  <div
    class="p-card new-playlist-card rounded"
    @click="Modal.showNewPlaylistModal()"
  >
    <PlusSvg />
  </div>
</template>

<script setup lang="ts">
import PlusSvg from "../../assets/icons/plus.svg";
import useModalStore from "../../stores/modal";

const Modal = useModalStore();
</script>

<style lang="scss">
.new-playlist-card {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;

  svg {
    transform: scale(3);
  }
}
</style>
