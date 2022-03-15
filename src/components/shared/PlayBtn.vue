<template>
  <div class="play-btn circular">
    <div class="icon"></div>
  </div>
</template>

<style lang="scss">
.play-btn {
  width: 2rem;
  height: 2rem;
  background-color: $accent;
  background-image: url("../../assets/icons/play.svg");
  background-size: 1.25rem;
  background-position: 60%;
  background-repeat: no-repeat;
  transition: all .25s;

  &:hover {
      background-color: rgb(58, 197, 58);
      transform: scale(1.1);
  }
}
</style>
