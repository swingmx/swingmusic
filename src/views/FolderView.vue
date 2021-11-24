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
  position: relative;
  height: 100%;
  background-color: #131313b2;
  padding-left: 1em;
  padding-right: 1em;
  padding-top: 5em;
}

#f-view-parent .fixed {
  position: absolute;
  height: min-content;
  width: calc(100% - 2em);
  top: .5em;
}

#scrollable {
  overflow-y: scroll;
  height: calc(100% - 5em);
  padding-right: 1em;
}
</style>