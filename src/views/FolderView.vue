<template>
  <div id="f-view-parent" class="border rounded">
    <div class="fixed">
      <Header :path="path" :first_song="songs[0]" @search="updateQueryString" />
    </div>
    <div id="scrollable" ref="scrollable">
      <FolderList :folders="folders" />
      <div class="separator" v-if="folders.length && songs.length"></div>
      <SongList :songs="songs" />
    </div>
  </div>
</template>

<script>
import { computed, ref } from "@vue/reactivity";
import { useRoute } from "vue-router";

import SongList from "@/components/FolderView/SongList.vue";
import FolderList from "@/components/FolderView/FolderList.vue";
import Header from "@/components/FolderView/Header.vue";

import getTracksAndDirs from "../composables/getFiles.js";
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

    const song_list = ref(state.folder_song_list);
    const folders_list = ref(state.folder_list);

    const scrollable = ref(null);

    const query = ref("");

    const songs = computed(() => {
      const songs_ = [];

      if (query.value.length > 1) {
        for (let i = 0; i < song_list.value.length; i++) {
          if (
            song_list.value[i].title
              .toLowerCase()
              .includes(query.value.toLowerCase())
          ) {
            songs_.push(song_list.value[i]);
          }
        }

        return songs_;
      } else {
        return song_list.value;
      }
    });

    const folders = computed(() => {
      const folders_ = [];

      if (query.value.length > 1) {
        for (let i = 0; i < folders_list.value.length; i++) {
          if (
            folders_list.value[i].name
              .toLowerCase()
              .includes(query.value.toLowerCase())
          ) {
            folders_.push(folders_list.value[i]);
          }
        }

        return folders_;
      } else {
        return folders_list.value;
      }
    });

    onMounted(() => {
      const getDirData = (path) => {
        state.loading.value = true;
        getTracksAndDirs(path)
          .then((data) => {
            scrollable.value.scrollTop = 0;

            state.folder_song_list.value = data.songs;
            state.folder_list.value = data.folders;

            state.loading.value = false;
          })
          .then(() => {
            setTimeout(() => {
              query.value = "";
            }, 100);
          });
      };

      getDirData(path.value);

      watch(
        () => route.params,
        () => {
          path.value = route.params.path;

          if (!path.value) return;

          getDirData(path.value);
        }
      );
    });

    function updateQueryString(value) {
      query.value = value;
    }

    return {
      updateQueryString,
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
