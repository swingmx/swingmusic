<template>
  <Header />
  <div class="p-bg rounded">
    <div class="clip">
      <div class="scrollable">
        <SongList />
      </div>
    </div>
    <div class="f-artists-p">
      <FeaturedArtists />
    </div>
  </div>
</template>

<script>
import Header from "@/components/PlaylistView/Header.vue";
import SongList from "@/components/PlaylistView/SongList.vue";
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

.p-bg .clip {
  height: calc(100% - 12em);
  padding-bottom: $small;
  border-bottom: solid 1px $separator;
}

.p-bg .scrollable {
  height: 100%;
  border-radius: $small;
}

.p-bg .f-artists {
  position: absolute;
  bottom: 0;
  margin-top: 1em;
}
</style>