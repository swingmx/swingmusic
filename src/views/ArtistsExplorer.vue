<template>
  <div class="a-container">
    <TopArtists />
    <Artists />
  </div>
</template>

<script>
import TopArtists from "../components/ArtistsExplorer/TopArtists.vue";
import Artists from "../components/ArtistsExplorer/ArtistsList.vue";

export default {
  components: {
    TopArtists,
    Artists
  },
};
</script>

<style lang="scss">
.a-container {
  height: 100%;
  border-radius: $small;
}
</style>