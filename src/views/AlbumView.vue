<template>
  <div class="al-view rounded">
    <div>
      <Header :album_info="album_info" />
    </div>
    <div class="separator" id="av-sep"></div>
    <div class="songs rounded">
      <SongList :songs="album_songs" />
    </div>
    <div class="separator" id="av-sep"></div>
    <FeaturedArtists :artists="artists" />
    <div class="separator" id="av-sep"></div>
    <AlbumBio />
    <div class="separator" id="av-sep"></div>
    <FromTheSameArtist />
  </div>
</template>

<script>
import { useRoute } from "vue-router";
import { onMounted } from "@vue/runtime-core";

import Header from "../components/AlbumView/Header.vue";
import AlbumBio from "../components/AlbumView/AlbumBio.vue";
import FromTheSameArtist from "../components/AlbumView/FromTheSameArtist.vue";

import SongList from "../components/FolderView/SongList.vue";
import FeaturedArtists from "../components/PlaylistView/FeaturedArtists.vue";

import album from "@/composables/album.js";
import state from "@/composables/state.js";
import { onUnmounted } from "@vue/runtime-core";

export default {
  components: {
    Header,
    AlbumBio,
    FromTheSameArtist,
    SongList,
    FeaturedArtists,
  },
  setup() {
    const route = useRoute();
    const title = route.params.album;
    const album_artists = route.params.artist;

    onMounted(() => {
      if (!state.album_song_list.value.length) {
        album.getAlbumTracks(title, album_artists).then((data) => {
          state.album_song_list.value = data.songs;
          state.album_info.value = data.info;

          state.loading.value = false;
        });
      }

      if (state.album_artists.value.length == 0) {
        album.getAlbumArtists(title, album_artists).then((data) => {
          state.album_artists.value = data;
          console.log(state.album_artists.value)
        });
      }
    });

    onUnmounted(() => {
      state.album_song_list.value = [];
      state.album_info.value = {};
      state.album_artists.value = [];
    });

    return {
      album_songs: state.album_song_list,
      album_info: state.album_info,
      artists: state.album_artists,
    };
  },
};
</script>

<style lang="scss">
.al-view {
  height: calc(100% - 1rem);
  overflow: auto;
  margin-top: $small;

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