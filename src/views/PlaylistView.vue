<template>
  <div class="playlist-view">
    <Header :playlist_info="playlist_info" />
    <div class="separator no-border"></div>

    <div class="songlist rounded">
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
import state from "@/composables/state";
export default {
  components: {
    Header,
    SongList,
    FeaturedArtists,
  },
  setup() {
    return {
      songs: state.queue,
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
    min-height: 100%;
  }
}
</style>
