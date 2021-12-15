<template>
  <div id="f-view-parent" class="rounded">
    <div class="fixed">
      <SearchBox />
    </div>
    <div id="scrollable">
      <SongList />
      <FolderList :folders="folders" />
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
import { useRoute } from 'vue-router'

import SongList from "@/components/FolderView/SongList.vue";
import FolderList from "@/components/FolderView/FolderList.vue";
import SearchBox from "@/components/FolderView/SearchBox.vue";

import getData from "../composables/getFiles.js";

export default {
  components: {
    SongList,
    FolderList,
    SearchBox,
  },
  setup() {
    const route = useRoute();

    const path = route.params.path;

    console.log(path);

    const songs = ref([]);
    const folders = ref([]);

    getData("/Music").then((data) => {
      songs.value = data.songs.value;
      folders.value = data.folders.value;
    });
    return {
      songs,
      folders,
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
  padding-right: 1rem;
}
</style>