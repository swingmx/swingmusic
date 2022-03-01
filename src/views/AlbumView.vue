<template>
  <div class="al-view rounded">
    <div>
      <Header :album_info="state.album.info" />
    </div>
    <div class="separator" id="av-sep"></div>
    <div class="songs rounded">
      <SongList :songs="state.album.tracklist" />
    </div>
    <div class="separator" id="av-sep"></div>
    <FeaturedArtists :artists="state.album.artists" />
    <div v-if="state.album.bio">
      <div class="separator" id="av-sep"></div>
      <AlbumBio :bio="state.album.bio" v-if="state.album.bio" />
    </div>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import { onMounted } from "@vue/runtime-core";
import { watch } from "vue";
import Header from "../components/AlbumView/Header.vue";
import AlbumBio from "../components/AlbumView/AlbumBio.vue";

import SongList from "../components/FolderView/SongList.vue";
import FeaturedArtists from "../components/PlaylistView/FeaturedArtists.vue";

import state from "@/composables/state.js";
import routeLoader from "@/composables/routeLoader.js";

const route = useRoute();

onMounted(() => {
  routeLoader.toAlbum(route.params.album, route.params.artist);

  watch(
    () => route.params,
    () => {
      if (route.name === "AlbumView") {
        routeLoader.toAlbum(route.params.album, route.params.artist);
      }
    }
  );
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
    min-height: calc(100% - 30rem);
  }

  &::-webkit-scrollbar {
    display: none;
  }

  #av-sep {
    border: none;
  }
}
</style>
