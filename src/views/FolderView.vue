<template>
  <div id="f-view-parent" class="rounded">
    <div class="fixed">
      <SearchBox :path="path" :loading="loading" />
    </div>
    <div id="scrollable" ref="scrollable">
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
import { onMounted, watch } from "@vue/runtime-core";

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
    const last_page = ref([]);
    const last_song_id = ref(null);

    const scrollable = ref(null);
    const loading = ref(false);

    onMounted(() => {
      const getPathFolders = (path, last_id) => {
        loading.value = true;
        getData(path, last_id).then((data) => {
          scrollable.value.scrollTop = 0;

          songs.value = data.songs.value;
          last_page.value = songs.value;

          if (songs.value.length) {
            last_song_id.value = songs.value.slice(-1)[0]._id.$oid;
          }

          folders.value = data.folders.value;
          loading.value = false;
        });
      };

      getPathFolders(path.value);

      watch(route, (new_route) => {
        path.value = new_route.params.path;
        getPathFolders(path.value);
      });
    });

    return {
      songs,
      folders,
      path,
      scrollable,
      loading,
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
  height: 100%;
  margin-top: $small;

  &::-webkit-scrollbar {
    display: none;
  }
}
</style>