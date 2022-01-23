<template>
  <div class="result-item border">
    <div
      class="album-art image"
      :style="{
        backgroundImage: `url(&quot;${album.image}&quot;)`,
      }"
    ></div>
    <div class="title ellip">{{ album.name }}</div>
    <div class="artistsx ellipsis">{{ album.artist }}</div>
  </div>
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