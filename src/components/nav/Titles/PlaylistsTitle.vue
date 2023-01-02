<template>
  <div class="playlists-nav">
    <SimpleNav :text="'Playlists'" />
    <div class="buttons">
      <button @click="showNewPlaylistModal()"><PlusSvg /> New Playlist</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import SimpleNav from "./SimpleNav.vue";
import PlusSvg from "../../../assets/icons/plus.svg";

import useModalStore from "@/stores/modal";
const { showNewPlaylistModal } = useModalStore();
</script>

<style lang="scss">
.playlists-nav {
  display: grid;
  grid-template-columns: 1fr max-content;

  button {
    padding-right: $small;
  }
}
</style>
