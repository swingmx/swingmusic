<template>
  <Header />
  <div class="p-bg rounded">
    <SongList />
  </div>
</template>

<script>
import Header from "@/components/PlaylistView/Header.vue";
import SongList from "@/components/FolderView/SongList.vue";

export default {
  components: {
    Header,
    SongList,
  },
  setup() {
    return {};
  },
};
</script>

<style lang="scss">
.p-bg {
  background: $card-dark;
  padding: 20px;
  height: calc(100% - 16em);
  padding: 0;
}
</style>