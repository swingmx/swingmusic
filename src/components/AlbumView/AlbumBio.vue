<template>
  <div class="al-bio rounded border card-dark">
    <div class="left rounded border">
      <div class="rect rounded"></div>
      <div class="circle"></div>
    </div>
    <div class="bio rounded border" v-html="bio"></div>
  </div>
</template>

<script>
export default {
  props: ['bio'],
};
</script>

<style lang="scss">
.al-bio {
  padding: $small;
  display: grid;
  grid-template-columns: 1fr 1fr;

  @include tablet-portrait {
    grid-template-columns: 1fr;
  }

  @include tablet-landscape {
    grid-template-columns: 1fr auto;
  }

  gap: $small;
  min-height: 15rem;

  .left {
    position: relative;
    height: 100%;
    width: 100%;
    margin-right: $small;
    overflow: hidden;
    background-image: url("../../assets/images/eggs.jpg");
    background-position: center;

    @include tablet-portrait {
      display: none;
    }

    @include tablet-landscape {
      width: 10rem;
    }


    .rect {
      width: 10rem;
      height: 10rem;
      position: absolute;
      background-color: rgb(196, 58, 58);
      box-shadow: 0px 0px 2rem rgb(0, 0, 0);
      bottom: -10rem;
      left: 7rem;
      transform: rotate(45deg) translate(-1rem, -9rem);
      z-index: 1;
      transition: all .5s ease-in-out;

      &:hover {
        transition: all .5s ease-in-out;
      }
    }

    .circle {
      width: 7rem;
      height: 7rem;
      position: absolute;
      right: 0;
      background-color: $blue;
      border-radius: 50%;
      transform: translateX(-11rem) translateY(7rem);
      box-shadow: 0px 0px 2rem rgb(0, 0, 0);
    }
  }
  .bio {
    padding: $small;
    line-height: 1.5rem;

    &::after {
      content: "...";
    }
  }
}
</style>