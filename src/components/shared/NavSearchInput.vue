<template>
  <div class="header-input-wrapper rounded-sm" :class="{ showInput: clicked }">
    <button
      class="search-btn circular"
      id="page-search-trigger"
      :class="{ 'btn-active': clicked }"
      @click="handleFocus"
    >
      <SearchSvg /> Search
    </button>
    <input
      class="header-input pad-sm"
      :class="{ showInput: clicked }"
      placeholder="Type to search"
      v-model.trim="query"
      id="page-search"
      ref="inputRef"
    />
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ref } from "vue";

import useAlbumStore from "@/stores/pages/album";
import useFolderStore from "@/stores/pages/folder";
import usePStore from "@/stores/pages/playlist";

import SearchSvg from "@/assets/icons/search.svg";
import { Routes } from "@/router/routes";

const clicked = ref(false);
const [playlist, album, folder] = [
  usePStore(),
  useAlbumStore(),
  useFolderStore(),
];

const { query: playlistQuery } = storeToRefs(playlist);
const { query: folderQuery } = storeToRefs(folder);
const { query: albumQuery } = storeToRefs(album);

const props = defineProps<{
  page: typeof Routes | string;
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
  &.showInput {
    width: 21.5rem;
  }

  display: flex;
  flex-direction: row-reverse;
  width: 7rem;
  gap: $small;
  transition: all 0.25s;
  transition-delay: 0.1s;
}

.header-input {
  background-color: transparent;
  border: none;
  color: inherit;
  font-size: 1rem;
  z-index: 200;
  transition: all 0.25s $overshoot;
  opacity: 0;
  transform: translateY(-3.5rem);
  border-radius: 3rem;
  padding-left: 1rem;
  outline: solid 1px $gray1;

  &:focus {
    outline: solid $darkblue;
  }

  &.showInput {
    opacity: 1;
    transform: translateY(0);
    transition-delay: 0.1s;
  }
}

.search-btn {
  cursor: pointer;
  padding: 0 $small;
  padding-right: 1rem;
}
</style>
