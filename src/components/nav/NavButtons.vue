<template>
  <div id="back-forward">
    <div class="back image" @click="$router.back()"></div>
    <div class="forward image" @click="$router.forward()"></div>
  </div>
</template>

<style lang="scss">
#back-forward {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  padding-right: 1rem;
  margin-right: $small;
  border-right: 1px solid $gray3;

  & > div {
    background-color: $gray4;
    border-radius: $small;
    height: 2.25rem;
    width: 2.25rem;
    cursor: pointer;
    background-size: 2rem;
    transition: all .25s ease-in-out;

    &:hover {
      background-color: $accent;
    }
  }

  .back {
    background-image: url("../../assets/icons/right-arrow.svg");
    transform: rotate(180deg);
  }

  .forward {
    background-image: url("../../assets/icons/right-arrow.svg");
  }
}
</style>
