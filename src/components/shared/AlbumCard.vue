<template>
  <router-link
    :to="{
      name: 'AlbumView',
      params: { album: album.name, artist: album.artist },
    }"
    class="result-item border"
  >
    <div
      class="album-art image"
      :style="{
        backgroundImage: `url(&quot;${album.image}&quot;)`,
      }"
    ></div>
    <div class="title ellip">{{ album.name }}</div>
    <div class="artistsx ellipsis">{{ album.artist }}</div>
  </router-link>
</template>

<script>
export default {
  props: ["album"],
};
</script>

<style lang="scss">
.result-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: $small;
  border-radius: $small;
  text-align: left !important;
  width: 9rem;
  // border: solid 1px red !important;

  .album-art {
    height: 7rem;
    width: 7rem;
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .title {
    width: 7rem;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
  }

  .artistsx {
    width: 7rem;
    display: flex;
    font-size: 0.8rem;
    text-align: left;
    color: rgba(40, 116, 216, 0.767);
  }
}
</style>
