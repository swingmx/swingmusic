<template>
  <div class="other-keys">
    <div class="keys rounded playlist image"></div>
    <div class="keys rounded heart"></div>
    <div class="keys rounded folder"></div>
  </div>
</template>

<style lang="scss">
.l_ .other-keys {
//   border: solid;
  height: 2.5rem;
  display: grid;
  grid-template-columns: repeat(3, 1fr);

  .keys {
    height: 2rem;
    width: 100%;
    background-size: 1.5rem;
    background-repeat: no-repeat;
    background-position: center;

    &:hover {
      background-color: $red;
    }
  }
  .playlist {
    background-image: url("../../../assets/icons/plus.svg");
  }
}
</style>
