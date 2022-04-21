<template>
  <div id="f-view-parent" class="rounded">
    <div id="scrollable" ref="scrollable">
      <FolderList :folders="FStore.dirs" />
      <div
        class="separator"
        v-if="FStore.dirs.length && FStore.tracks.length"
      ></div>
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
import state from "../composables/state";
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
  padding: 0 $small 0 $small;
  overflow: hidden;
  margin: $small;
  margin-top: $small;

  .h {
    font-size: 2rem;
    font-weight: bold;
  }
}

// #f-view-parent .fixed {
//   position: absolute;
//   height: min-content;
//   width: calc(100% - 1rem);
//   top: 0.5rem;
// }

#scrollable {
  overflow-y: auto;
  height: calc(100% - $small);
  padding-right: $small;
  scrollbar-color: grey transparent;

  @include phone-only {
    padding-right: 0;

    &::-webkit-scrollbar {
      display: none;
    }
  }
}
</style>
