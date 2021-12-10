<template>
  <div class="a-container">
    <TopAlbums />
  </div>
</template>

<script>
import TopAlbums from "../components/AlbumsExplorer/TopAlbums.vue";

export default {
  components: {
    TopAlbums,
  },
};
</script>

<style lang="scss">
.a-container {
  height: 100%;
  border-radius: $small;
  background-color: $card-dark;
  padding: $small;
}
</style>