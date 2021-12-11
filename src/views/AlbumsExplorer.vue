<template>
  <div class="a-container">
    <TopAlbums />
    <Albums />
  </div>
</template>

<script>
import TopAlbums from "../components/AlbumsExplorer/TopAlbums.vue";
import Albums from "../components/AlbumsExplorer/AlbumList.vue";

export default {
  components: {
    TopAlbums,
    Albums
  },
};
</script>

<style lang="scss">
.a-container {
  height: 100%;
  border-radius: $small;
}
</style>