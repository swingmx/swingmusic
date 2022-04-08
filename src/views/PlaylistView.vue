<template>
  <div class="playlist-view">
    <Header :info="playlist.info" />
    <div class="separator no-border"></div>

    <div class="songlist rounded">
      <div v-if="playlist.tracks.length">
        <SongList
          :tracks="playlist.tracks"
          :pname="playlist.info.name"
          :playlistid="playlist.info.playlistid"
        />
      </div>
      <div v-else-if="playlist.tracks.length === 0 && playlist.info.count > 0">
        <div class="no-results">
          <div class="text">We can't find your music 🦋</div>
        </div>
      </div>
      <div v-else-if="playlist.tracks.length === 0 && playlist.info.count == 0">
        <div class="no-results">
          <div class="text">Nothing here</div>
        </div>
      </div>
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
