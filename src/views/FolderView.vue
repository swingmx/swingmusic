<template>
  <div id="f-view-parent">
    <div id="scrollable" ref="scrollable">
      <FolderList :folders="FStore.dirs" />
      <SongList :tracks="FStore.tracks" :path="FStore.path" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "@vue/reactivity";
import { onBeforeRouteUpdate } from "vue-router";

import SongList from "@/components/FolderView/SongList.vue";
import FolderList from "@/components/FolderView/FolderList.vue";

import useFStore from "../stores/folder";
import useLoaderStore from "../stores/loader";

const loader = useLoaderStore();
const FStore = useFStore();

const scrollable = ref(null);

onBeforeRouteUpdate((to) => {
  loader.startLoading();
  FStore.fetchAll(to.params.path)
    .then(() => {
      scrollable.value.scrollTop = 0;
    })
    .then(() => {
      loader.stopLoading();
    });
});
</script>

<style lang="scss">
#f-view-parent {
  position: relative;

  .h {
    font-size: 2rem;
    font-weight: bold;
  }
}

#scrollable {
  overflow-y: auto;
  height: calc(100% - $small);
  scrollbar-color: grey transparent;

  @include phone-only {
    padding-right: 0;

    &::-webkit-scrollbar {
      display: none;
    }
  }
}
</style>
