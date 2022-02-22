<template>
  <div class="morexx">
    <button @click="loadMore" class="theme">
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
    height: 2.5rem;
    width: 10rem;
    display: grid;
  }
}
</style>