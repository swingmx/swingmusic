<template>
  <Header />
  <div class="p-bg rounded">
    <SongList />
    <div class="f-artists-p">
      <FeaturedArtists />
    </div>
  </div>
</template>

<script>
import Header from "@/components/PlaylistView/Header.vue";
import SongList from "@/components/FolderView/SongList.vue";
import FeaturedArtists from "@/components/PlaylistView/FeaturedArtists.vue";

export default {
  components: {
    Header,
    SongList,
    FeaturedArtists,
  },
  setup() {
    return {};
  },
};
</script>

<style lang="scss">
.p-bg {
  position: relative;
  background: $card-dark;
  height: calc(100% - 16em);
  padding: $small;
}

.p-bg .f-artists {
  position: absolute;
  bottom: 0;
  margin-top: 1em;
}
</style>