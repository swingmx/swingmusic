<template>
  <div id="f-view-parent" class="rounded">
    <div class="fixed">
      <SearchBox :path="path"/>
    </div>
    <div id="scrollable" ref="scrollable">
      <FolderList :folders="folders" />
    <div class="separator"></div>
      <SongList :songs="songs" />
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
import { useRoute } from "vue-router";

import SongList from "@/components/FolderView/SongList.vue";
import FolderList from "@/components/FolderView/FolderList.vue";
import SearchBox from "@/components/FolderView/SearchBox.vue";

import getData from "../composables/getFiles.js";
import { onMounted, watch } from "@vue/runtime-core";
import state from "@/composables/state.js";

export default {
  components: {
    SongList,
    FolderList,
    SearchBox,
  },
  setup() {
    const route = useRoute();
    const path = ref(route.params.path);

    const songs = ref([]);
    const folders = ref([]);

    const scrollable = ref(null);

    function focusSearch() {
      console.log("focusSearch");
    }

    onMounted(() => {
      const getPathFolders = (path, last_id) => {
        state.loading.value = true;
        getData(path, last_id).then((data) => {
          scrollable.value.scrollTop = 0;

          songs.value = data.songs;
          folders.value = data.folders;

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
  height: 100%;
  background-color: $card-dark;
  padding-left: $small;
  padding-right: $small;
  padding-top: 5rem;
  overflow: hidden;
}

#f-view-parent .fixed {
  position: absolute;
  height: min-content;
  width: calc(100% - 2rem);
  top: 0.5rem;
}

#scrollable {
  overflow-y: scroll;
  height: calc(100% - $small);
  padding-right: $small;

  .separator {
    margin: 0 1rem 0 1rem;
  }
}
</style>