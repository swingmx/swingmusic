<template>
  <div>
    <SongList/>
    <!-- <hr> -->
    <FolderList/>
  </div>
</template>

<script>
import SongList from "@/components/FolderView/SongList.vue";
import FolderList from "@/components/FolderView/FolderList.vue";

export default {
  components: {
    SongList,
    FolderList
  },
  setup() {
    return {
      //
    };
  },
};
</script>

<style>
  
</style>