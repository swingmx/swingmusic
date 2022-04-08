<template>
  <div class="p-card rounded" id="new-playlist-card">
    <div class="gradient rounded"></div>
    <div class="plus image p-image"></div>
    <div>New Playlist</div>
  </div>
</template>

<style lang="scss">
#new-playlist-card {
  display: grid;
  place-items: center;
  background-color: $black;
  position: relative;
  cursor: pointer;

  .gradient {
    position: absolute;
    width: calc(100% - 2rem);
    height: 10rem;
    top: 1rem;
    background-image: linear-gradient(37deg, $red, $blue);
    background-size: 100%;
    transition: all .5s ease-in-out;
  }

  .image {
    background-image: url("../../assets/icons/plus.svg");
    background-size: 5rem;
    z-index: 1;
    transition: all .5s ease-in-out;
  }

  &:hover {
    .gradient {
      background-size: 30rem;
    }
    .image {
      transform: rotate(270deg);
    }
  }
}
</style>
