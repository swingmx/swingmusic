<template>
  <router-link
    :to="{
      name: 'AlbumView',
      params: { album: album.name, artist: album.artist },
    }"
    class="result-item"
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
  border-radius: .75rem;
  text-align: left !important;
  background-color: #726c7227;

  &:hover {
    background-color: #1b3688cb;
  }

  .album-art {
    height: 7.5rem;
    width: 7.5rem;
    border-radius: .5rem;
    margin-bottom: 0.5rem;
  }

  .title {
    width: 7rem;
    margin-bottom: 0.25rem;
    font-size: 0.9rem;
  }

  .artistsx {
    width: 7rem;
    font-size: 0.8rem;
    text-align: left;
    color: #ffffffbd;
  }
}
</style>
