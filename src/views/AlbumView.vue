<template>
  <div class="al-view rounded">
    <div>
      <Header :album_info="album_info" />
    </div>
    <div class="separator" id="av-sep"></div>
    <div class="songs rounded border">
      <SongList :songs="album_songs" />
    </div>
    <div class="separator" id="av-sep"></div>
    <FeaturedArtists :artists="artists" />
    <div class="separator" id="av-sep"></div>
    <AlbumBio :bio="bio" v-if="bio" />
    <div class="separator" id="av-sep"></div>
  </div>
</template>

<script>
import { useRoute } from "vue-router";
import { onMounted } from "@vue/runtime-core";
import { onUnmounted } from "@vue/runtime-core";
import { watch } from "vue";
import Header from "../components/AlbumView/Header.vue";
import AlbumBio from "../components/AlbumView/AlbumBio.vue";

import SongList from "../components/FolderView/SongList.vue";
import FeaturedArtists from "../components/PlaylistView/FeaturedArtists.vue";

import state from "@/composables/state.js";
import routeLoader from "@/composables/routeLoader.js";

export default {
  components: {
    Header,
    AlbumBio,
    SongList,
    FeaturedArtists,
  },
  setup() {
    const route = useRoute();

    watch(
      () => route.params,
      () => {
        if (route.name === "AlbumView") {
          routeLoader.toAlbum(route.params.album, route.params.artist);
        }
      }
    );

    onMounted(() => {
      console.log("mounted");
      routeLoader.toAlbum(route.params.album, route.params.artist);
    });

    onUnmounted(() => {
      state.album_song_list.value = [];
      state.album_info.value = {};
      state.album_artists.value = [];
      state.album_bio.value = "";
    });

    return {
      album_songs: state.album_song_list,
      album_info: state.album_info,
      artists: state.album_artists,
      bio: state.album_bio,
    };
  },
};
</script>

<style lang="scss">
.al-view {
  height: calc(100% - 1rem);
  overflow: auto;
  margin: $smaller $small;
  scrollbar-width: none;

  .songs {
    padding: $small;
    background-color: $card-dark;
  }

  &::-webkit-scrollbar {
    display: none;
  }

  #av-sep {
    border: none;
  }
}
</style>