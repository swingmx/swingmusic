<template>
  <div class="playbtnrect rounded">
    <div class="icon image"></div>
    <div class="text">Play</div>
  </div>
</template>

<style lang="scss">
.playbtnrect {
  width: 6rem;
  display: flex;
  align-items: center;
  height: 2.5rem;
  padding-left: 0.75rem;
  cursor: pointer;
  background: linear-gradient(34deg, $indigo, $pink);
  user-select: none;
  transition: all 0.5s ease;

  .icon {
    height: 2rem;
    width: 2rem;
    background-image: url("../../assets/icons/play.svg");
  }

  &:hover {
    .icon {
        transform: rotate(120deg);
    }
  }
}
</style>
