<template>
  <div class="al-view">
    <div class="header">
      <Header />
    </div>
    <div class="separator" id="av-sep"></div>
    <div>
      <SongList />
    </div>
    <div class="separator" id="av-sep"></div>
    <FeaturedArtists />
  </div>
</template>

<script>
import Header from "../components/AlbumView/Header.vue";
import SongList from "../components/PlaylistView/SongList.vue";
import FeaturedArtists from "../components/PlaylistView/FeaturedArtists.vue";

export default {
  components: {
    Header,
    SongList,
    FeaturedArtists,
  },
};
</script>

<style lang="scss">
.al-view {
  height: 100%;
  overflow: auto;

  .header {
    position: sticky;
    top: 0;
    z-index: 60;
  }

  &::-webkit-scrollbar {
    display: none;
  }

  #av-sep {
    border: none;
  }
}
</style>