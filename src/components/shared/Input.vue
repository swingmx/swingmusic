<template>
  <div class="header-input-wrapper rounded-sm" :class="{ showInput: clicked }">
    <div class="search-svg" @click="handleFocus">
      <SearchSvg />
    </div>
    <input
      type="search"
      class="header-input rounded-sm pad-sm"
      :class="{ showInput: clicked }"
      placeholder="Search here"
      v-model.trim="query"
      id="page-search"
      ref="inputRef"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { storeToRefs } from "pinia";

import usePStore from "@/stores/pages/playlist";
import useAlbumStore from "@/stores/pages/album";
import useFolderStore from "@/stores/pages/folder";

import { Routes } from "@/composables/enums";
import SearchSvg from "@/assets/icons/search.svg";

const clicked = ref(true);
const [playlist, album, folder] = [
  usePStore(),
  useAlbumStore(),
  useFolderStore(),
];

const { query: playlistQuery } = storeToRefs(playlist);
const { query: folderQuery } = storeToRefs(folder);
const { query: albumQuery } = storeToRefs(album);

const props = defineProps<{
  page: Routes | string;
}>();
const inputRef = ref<HTMLElement>();

function handleFocus() {
  // if input is not focused, focus it
  // if input is focused, blur it
  clicked.value = !clicked.value;
  if (clicked.value) {
    inputRef.value?.focus();
  } else {
    inputRef.value?.blur();
    resetQuery();
  }
}

function getRef() {
  switch (props.page) {
    case Routes.playlist:
      return [playlistQuery, playlist.resetQuery];

    case Routes.folder:
      return [folderQuery, folder.resetQuery];

    case Routes.album:
      return [albumQuery, album.resetQuery];

    default:
      return null;
  }
}

const source = getRef();
let query: any;
let resetQuery: any;

if (source) {
  query = source[0];
  resetQuery = source[1];
}
</script>

<style lang="scss">
.header-input-wrapper {
  display: flex;
  flex-direction: row-reverse;
  width: 1.5rem;
  transition: all 0.25s;

  &.showInput {
    width: 15rem;
  }
}

.header-input {
  background-color: $gray3;
  outline: none;
  border: none;
  color: inherit;
  font-size: 1rem;
  z-index: 200;
  transition: all 0.25s $overshoot;
  opacity: 0;
  transform: translateY(-1rem);

  &:focus {
    outline: solid;
  }

  &.showInput {
    opacity: 1;
    transform: translateY(0);
    transition-delay: 0.1s;
  }
}

.search-svg {
  margin-top: $smaller;
  cursor: pointer;
  width: 2.25rem;
  height: 2rem;
  z-index: 100;

  svg {
    display: block;
    margin: 0 auto;
  }
}
</style>
