<template>
  <div class="al-view rounded">
    <div>
      <Header :album="album.info" />
    </div>
    <div class="separator" id="av-sep"></div>
    <div class="songs rounded">
      <SongList :tracks="album.tracks" />
    </div>
    <div class="separator" id="av-sep"></div>
    <FeaturedArtists :artists="album.artists" />
    <div v-if="album.bio">
      <div class="separator" id="av-sep"></div>
      <AlbumBio :bio="album.bio" />
    </div>
  </div>
</template>

<script setup lang="ts">
import Header from "../components/AlbumView/Header.vue";
import AlbumBio from "../components/AlbumView/AlbumBio.vue";

import SongList from "../components/FolderView/SongList.vue";
import FeaturedArtists from "../components/PlaylistView/FeaturedArtists.vue";

import useAStore from "../stores/album";
import { onBeforeRouteUpdate } from "vue-router";

const album = useAStore();

onBeforeRouteUpdate(async (to) => {
  await album.fetchTracksAndArtists(
    to.params.album.toString(),
    to.params.artist.toString()
  );
  album.fetchBio(to.params.album.toString(), to.params.artist.toString());
});
</script>

<style lang="scss">
.al-view {
  height: calc(100% - 1rem);
  overflow: auto;
  margin: $small $small;
  scrollbar-width: none;

  .songs {
    padding: $small;
    min-height: calc(100% - 32rem);
  }

  &::-webkit-scrollbar {
    display: none;
  }

  #av-sep {
    border: none;
  }
}
</style>
