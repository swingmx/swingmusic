<template>
  <div class="header-input-wrapper rounded-sm" :class="{ showInput: clicked }">
    <div class="search-svg" @click="clicked = !clicked">
      <SearchSvg />
    </div>
    <input
      type="search"
      class="header-input rounded-sm pad-sm"
      :class="{ showInput: clicked }"
      placeholder="Search here"
      v-model.trim="source"
      id="page-search"
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

const clicked = ref(false);

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
    transition-delay: .1s;
  }
}

.search-svg {
  // outline: solid;
  margin-top: $smaller;
  cursor: pointer;
  // padding-left: ;
  width: 2.25rem;
  height: 2rem;
  // aspect-ratio: 1;
  z-index: 100;

  svg {
    display: block;
    margin: 0 auto;
    // outline: solid;
  }
}
</style>
