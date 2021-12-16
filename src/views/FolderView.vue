<template>
  <div id="f-view-parent" class="rounded">
    <div class="fixed">
      <SearchBox :path="path"/>
    </div>
    <div id="scrollable">
      <FolderList :folders="folders" />
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
import { watch } from "@vue/runtime-core";

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

    const getPathFolders = (path) => {
      getData(path).then((data) => {
        document.getElementById('scrollable').scrollTop = 0;
        songs.value = data.songs.value;
        folders.value = data.folders.value;
      });
    };

    getPathFolders(path.value);

    watch(route, (new_route) => {
      path.value = new_route.params.path;
      getPathFolders(encodeURI(path.value));
    });

    return {
      songs,
      folders,
      path
    };
  },
};
</script>

<style lang="scss">
#f-view-parent {
  position: relative;
  height: 100%;
  background-color: #131313b2;
  padding-left: $small;
  padding-right: $small;
  padding-top: 5rem;
}

#f-view-parent .fixed {
  position: absolute;
  height: min-content;
  width: calc(100% - 2rem);
  top: 0.5rem;
}

#scrollable {
  overflow-y: scroll;
  height: 100%;
  padding: $small 1rem 0 0;
}
</style>