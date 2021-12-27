<template>
  <div class="al-view rounded">
    <div class="header">
      <Header :album_info="album_info"/>
    </div>
    <div class="separator" id="av-sep"></div>
    <div>
      <SongList :album_songs="album_songs"/>
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
import { useRoute } from "vue-router";
import { onMounted, ref } from "@vue/runtime-core";

import Header from "../components/AlbumView/Header.vue";
import AlbumBio from "../components/AlbumView/AlbumBio.vue";
import FromTheSameArtist from "../components/AlbumView/FromTheSameArtist.vue";

import SongList from "../components/PlaylistView/SongList.vue";
import FeaturedArtists from "../components/PlaylistView/FeaturedArtists.vue";

import getAlbum from "../composables/getAlbum.js";

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
    const album_name = route.params.album;
    const album_songs = ref([]);
    const album_info = ref({});

    onMounted(() => {
      getAlbum(album_name).then((data) => {
        album_songs.value = data.songs;
        album_info.value = data.info;
      });
    });

    return {
      album_songs,
      album_info,
    };
  },
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