<template>
  <div id="f-view-parent" class="rounded">
    <div class="fixed">
      <SearchBox />
    </div>
    <div id="scrollable">
      <SongList />
      <FolderList />
    </div>
  </div>
</template>

<script>
import SongList from "@/components/FolderView/SongList.vue";
import FolderList from "@/components/FolderView/FolderList.vue";
import SearchBox from "@/components/FolderView/SearchBox.vue";

export default {
  components: {
    SongList,
    FolderList,
    SearchBox,
  },
  setup() {
    return {
      //
    };
  },
};
</script>

<style>
#f-view-parent {
  height: 99%;
  background-color: rgba(0, 0, 0, 0.24);
  padding-left: 20px;
  padding-right: 20px;
  padding-top: 1em;
}

#f-view-parent .fixed {
  height: min-content;
}
#scrollable {
  overflow-y: auto;
  height: 90%;
  margin-bottom: 2em;
}
</style>