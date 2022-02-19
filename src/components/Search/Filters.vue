<template>
  <div class="filter">
    <div
      class="item"
      v-for="filter in filters"
      :key="filter"
      @click="removeFilter(filter)"
    >
      {{ filter }}<span class="cancel image"></span>
    </div>
  </div>
</template>

<script>
export default {
  props: ["filters"],
  setup(props, { emit }) {
    const removeFilter = (filter) => {
      emit("removeFilter", filter);
    };

    return {
      removeFilter,
    };
  },
};
</script>

<style lang="scss">
.right-search .filter {
  display: flex;
  height: 2rem;

  .item {
    transition: all 0.2s ease-in-out;
    &:hover {
      width: 4rem;

      .cancel {
        position: absolute;
        right: 0.5rem;
        width: 1.5rem;
        height: 1.5rem;
        background-image: url(../../assets/icons/a.svg);
        background-size: 70%;
      }
    }
  }
}
</style>
