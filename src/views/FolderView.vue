<template>
  <div id="f-view-parent" class="rounded">
    <div class="fixed">
      <Header :path="FStore.path" :first_song="FStore.tracks[0]" />
    </div>
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
import Header from "@/components/FolderView/Header.vue";

import useFStore from "../stores/folder";
import state from "../composables/state";

const FStore = useFStore();

const scrollable = ref(null);

onBeforeRouteUpdate((to) => {
  state.loading.value = true;
  FStore.fetchAll(to.params.path)
    .then(() => {
      scrollable.value.scrollTop = 0;
    })
    .then(() => {
      state.loading.value = false;
    });
});
</script>

<style lang="scss">
#f-view-parent {
  position: relative;
  padding: 4rem $small 0 $small;
  overflow: hidden;
  margin: $small;

  .h {
    font-size: 2rem;
    font-weight: bold;
  }
}

#f-view-parent .fixed {
  position: absolute;
  height: min-content;
  width: calc(100% - 1rem);
  top: 0.5rem;
}

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
