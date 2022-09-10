<template>
  <input
    type="search"
    class="header-input rounded-sm pad-sm"
    placeholder="search here"
    v-model.trim="source"
    id="page-search"
  />
</template>

<script setup lang="ts">
import usePStore from "@/stores/pages/playlist";
import useFolderStore from "@/stores/pages/folder";
import useAlbumStore from "@/stores/pages/album";

import { storeToRefs } from "pinia";
import { Routes } from "@/composables/enums";

const { query: playlistQuery } = storeToRefs(usePStore());
const { query: folderQuery } = storeToRefs(useFolderStore());
const { query: albumQuery } = storeToRefs(useAlbumStore());

const props = defineProps<{
  page: Routes | string;
}>();

function getRef() {
  switch (props.page) {
    case Routes.playlist:
      return playlistQuery;

    case Routes.folder:
      return folderQuery;

    case Routes.album:
      return albumQuery;

    default:
      return null;
  }
}

const source = getRef();
</script>

<style lang="scss">
.header-input {
  background-color: $gray3;
  outline: none;
  border: none;
  color: inherit;
  font-size: 1rem;
  z-index: 200;

  &:focus {
    outline: solid;
  }
}
</style>
