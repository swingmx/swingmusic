<template>
  <div class="xartist" :style="{ backgroundColor: `#${color}` }">
    <div
      class="artist-image image border-sm"
      :style="{ backgroundImage: `url('${artist.image}')` }"
    ></div>
    <div>
      <p class="artist-name ellipsis">{{ artist.name }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: ["artist", "color"],
};
</script>

<style lang="scss">
.xartist {
  flex: 0 0 auto;
  overflow: hidden;
  position: relative;

  width: 9em;
  height: 11em;
  border-radius: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background-color: transparent;

  .artist-image {
    width: 7em;
    height: 7em;
    border-radius: 60%;
    margin-bottom: $small;
    background-size: 7rem 7rem;
    background-position: center;
    background-repeat: no-repeat;
    transition: all 0.5s ease-in-out;
  }

  &:hover {
    .artist-image {
      background-position: 50% 20%;
      border-radius: 20%;
      background-size: 10rem 10rem;
    }
  }

  .artist-name {
    margin: 0;
    text-align: center;
    font-size: 0.9rem;
    font-weight: 510;
    max-width: 7rem;
  }
}
</style>
