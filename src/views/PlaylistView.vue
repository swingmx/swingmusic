<template>
  <div class="playlist-view rounded">
    <Header :playlist_info="playlist_info" />
    <div class="separator no-border"></div>

    <div class="songlist rounded border">
      <SongList :songs="songs" />
    </div>
    <div class="separator no-border"></div>
    <FeaturedArtists />
  </div>
</template>

<script>
import Header from "@/components/PlaylistView/Header.vue";
import SongList from "@/components/FolderView/SongList.vue";
import FeaturedArtists from "@/components/PlaylistView/FeaturedArtists.vue";
import state from "@/composables/state.js";
export default {
  components: {
    Header,
    SongList,
    FeaturedArtists,
  },
  setup() {
    return {
      songs: state.folder_song_list,
      playlist_info: {
        name: "Dax Radio",
        count: state.folder_song_list.value.length,
        duration: "0:00",
        image: "../../assets/images/null.webp",
        artist: "",
        artist_image: "",
      },
    };
  },
};
</script>

<style lang="scss">
.playlist-view {
  height: calc(100% - 1rem);
  margin-top: $small;
  overflow: auto;

  &::-webkit-scrollbar {
    display: none;
  }
  .songlist {
    background-color: $card-dark;
    padding: $small;
    min-height: 100%;
  }
}
</style>