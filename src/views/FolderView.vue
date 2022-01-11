<template>
  <div id="f-view-parent" class="rounded">
    <div class="fixed">
      <Header :path="path" />
    </div>
    <div id="scrollable" ref="scrollable">
      <FolderList :folders="folders" />
      <div class="separator" v-if="folders.length && songs.length"></div>
      <SongList :songs="songs" />
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
import { useRoute } from "vue-router";

import SongList from "@/components/FolderView/SongList.vue";
import FolderList from "@/components/FolderView/FolderList.vue";
import Header from "@/components/FolderView/Header.vue";

import getData from "../composables/getFiles.js";
import { onMounted, watch } from "@vue/runtime-core";
import state from "@/composables/state.js";

export default {
  components: {
    SongList,
    FolderList,
    Header,
  },
  setup() {
    const route = useRoute();
    const path = ref(route.params.path);

    const songs = ref(state.song_list);
    const folders = ref(state.folder_list);

    const scrollable = ref(null);

    function focusSearch() {
      console.log("focusSearch");
    }

    onMounted(() => {
      const getPathFolders = (path, last_id) => {
        state.loading.value = true;
        getData(path, last_id).then((data) => {
          scrollable.value.scrollTop = 0;

          state.song_list.value = data.songs;
          state.folder_list.value = data.folders;

          state.loading.value = false;
        });
      };

      getPathFolders(path.value);

      watch(route, (new_route) => {
        state.search_query.value = "";
        path.value = new_route.params.path;
        getPathFolders(path.value);
      });
    });

    return {
      focusSearch,
      songs,
      folders,
      path,
      scrollable,
    };
  },
};
</script>

<style lang="scss">
#f-view-parent {
  position: relative;
  background-color: $card-dark;
  padding: 4rem $small 0 $small;
  overflow: hidden;
  margin: $small 0 $small 0;
}

#f-view-parent .fixed {
  position: absolute;
  height: min-content;
  width: calc(100% - 1rem);
  top: 0.5rem;

}

#scrollable {
  overflow-y: scroll;
  height: calc(100% - $small);
  padding-right: $small;
}
</style>