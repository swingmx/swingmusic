<template>
  <div class="morexx">
    <button @click="loadMore" class="">
      <div class="text">Load More</div>
    </button>
  </div>
</template>

<script>
export default {
  setup(props, { emit }) {
    function loadMore() {
      emit("loadMore");
    }

    return {
      loadMore,
    };
  },
};
</script>

<style lang="scss">
.morexx {
  display: grid;
  place-items: center;
  margin-top: $small;

  button {
    border-radius: 1.5rem;
    height: 2.5rem;
    width: 15rem;
    display: grid;
    transition: all 0.5s ease;
    color: rgba(255, 255, 255, 0.87) !important;
    background-color: transparent;
    border: solid 1px $gray;

    &:hover {
      background-color: $gray !important;
      width: 50%;
    }
  }
}
</style>