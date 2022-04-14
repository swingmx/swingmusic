<template>
  <div class="p-card rounded" id="new-playlist-card">
    <div class="gradient rounded"></div>
    <div class="plus image p-image"></div>
    <div>New Playlist</div>
    <div></div>
  </div>
</template>

<style lang="scss">
#new-playlist-card {
  display: grid;
  place-items: center;
  position: relative;
  cursor: pointer;

  .gradient {
    position: absolute;
    width: calc(100% - 1.5rem);
    top: 0.75rem;
    background-image: linear-gradient(37deg, $red, $blue);
    background-size: 100%;
    transition: all 0.5s ease-in-out;
    aspect-ratio: 1;
  }

  .image {
    background-image: url("../../assets/icons/plus.svg");
    background-size: 5rem;
    z-index: 1;
    transition: all 0.5s ease-in-out;
    background-color: transparent;
    margin-bottom: $small;
  }

  &:hover {
    .gradient {
      background-size: 300rem;
    }
    .image {
      transform: rotate(270deg);
    }
  }
}
</style>
