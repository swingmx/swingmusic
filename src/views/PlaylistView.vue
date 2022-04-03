<template>
  <div class="playlist-view">
    <Header :info="playlist.info" />
    <div class="separator no-border"></div>

    <div class="songlist rounded">
      <SongList
        :tracks="playlist.tracks"
        :pname="playlist.info.name"
        :playlistid="playlist.info.playlistid"
      />
    </div>
    <div class="separator no-border"></div>
    <FeaturedArtists />
  </div>
</template>

<script setup lang="ts">
import Header from "../components/PlaylistView/Header.vue";
import SongList from "../components/FolderView/SongList.vue";
import FeaturedArtists from "../components/PlaylistView/FeaturedArtists.vue";
import usePTrackStore from "../stores/p.ptracks";

const playlist = usePTrackStore();
</script>

<style lang="scss">
.playlist-view {
  height: calc(100% - 0rem);
  margin: 0 $small;
  overflow: auto;
  padding-bottom: $small;
  scrollbar-width: none;

  &::-webkit-scrollbar {
    display: none;
  }
  .songlist {
    padding: $small;
    min-height: calc(100% - 30rem);
  }
}
</style>
