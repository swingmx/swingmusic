<template>
  <div class="al-view rounded">
    <div class="header">
      <Header />
    </div>
    <div class="separator" id="av-sep"></div>
    <div>
      <SongList />
    </div>
    <div class="separator" id="av-sep"></div>
    <FeaturedArtists />
    <div class="separator" id="av-sep"></div>
    <AlbumBio />
    <div class="separator" id="av-sep"></div>
    <FromTheSameArtist />
  </div>
</template>

<script>
// import { useRoute } from 'vue-router'

import Header from "../components/AlbumView/Header.vue";
import AlbumBio from "../components/AlbumView/AlbumBio.vue";
import FromTheSameArtist from "../components/AlbumView/FromTheSameArtist.vue";

import SongList from "../components/PlaylistView/SongList.vue";
import FeaturedArtists from "../components/PlaylistView/FeaturedArtists.vue";

export default {
  components: {
    Header,
    AlbumBio,
    FromTheSameArtist,
    SongList,
    FeaturedArtists,
  },
  setup() {},
};
</script>

<style lang="scss">
.al-view {
  height: 100%;
  overflow: auto;

  &::-webkit-scrollbar {
    display: none;
  }

  #av-sep {
    border: none;
  }
}
</style>