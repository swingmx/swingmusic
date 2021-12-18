<template>
  <div id="f-view-parent" class="rounded">
    <div class="fixed">
      <SearchBox :path="path" />
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

    const scrollable = ref(null);

    const last_song_id = ref(null);
    const last_page = ref([]);

    onMounted(() => {
      const getPathFolders = (path, last_id) => {
        getData(path, last_id).then((data) => {
          scrollable.value.scrollTop = 0;

          songs.value = data.songs.value;
          last_page.value = songs.value;

          if (songs.value.length) {
            last_song_id.value = songs.value.slice(-1)[0]._id.$oid;
          }

          folders.value = data.folders.value;
        });
      };

      getPathFolders(path.value);

      watch(route, (new_route) => {
        path.value = new_route.params.path;
        getPathFolders(encodeURI(path.value));
      });

      scrollable.value.onscroll = () => {
        let dom = scrollable.value;

        let scrollY = dom.scrollHeight - dom.scrollTop;
        let height = dom.offsetHeight;
        let offset = height - scrollY;

        if (offset == 0 || offset == 1) {
          getData(path.value, last_song_id.value).then((data) => {
            songs.value = songs.value.concat(data.songs.value);

            if (songs.value.length) {
              last_song_id.value = songs.value.slice(-1)[0]._id.$oid;
            }
          });
        }
      };
    });

    return {
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

  &::-webkit-scrollbar {
    display: none;
  }
}
</style>