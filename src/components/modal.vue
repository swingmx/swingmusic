<template>
  <div class="new-playlist-modal" v-if="modal.visible">
    <div class="bg" @click="modal.hideModal"></div>
    <div class="m-content rounded">
      <div class="heading">{{ modal.title }}</div>
      <div class="cancel image" @click="modal.hideModal"></div>
      <NewPlaylist
        v-if="modal.component == modal.options.newPlaylist"
        :track="modal.props.track"
        @hideModal="hideModal"
        @title="title"
      />
      <UpdatePlaylist
        :playlist="modal.props"
        v-if="modal.component == modal.options.updatePlaylist"
        @hideModal="hideModal"
        @title="title"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import useModalStore from "../stores/modal";
import NewPlaylist from "./modals/NewPlaylist.vue";
import UpdatePlaylist from "./modals/updatePlaylist.vue";

const modal = useModalStore();

/**
 * Sets the modal title
 * @param title
 */
function title(title: string) {
  console.log(title);
  modal.setTitle(title);
}

/**
 * Handle the emit to hide the modal
 */
function hideModal() {
  modal.hideModal();
}
</script>

<style lang="scss">
.new-playlist-modal {
  position: fixed;
  z-index: 20;
  height: 100vh;
  width: 100vw;
  display: grid;
  place-items: center;

  .bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(12, 12, 12, 0.767);
  }

  .m-content {
    width: 30rem;
    background-color: $black;
    padding: 1rem;
    position: relative;

    .cancel {
      width: 2rem;
      height: 2rem;
      position: absolute;
      top: 1rem;
      right: 1rem;
      background-image: url("../assets/icons/plus.svg");
      transform: rotate(45deg);

      &:hover {
        cursor: pointer;
        transform: rotate(135deg);
      }
    }
  }
}
</style>
