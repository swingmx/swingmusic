<template>
  <div class="gsearch-input">
    <Filters :filters="search.filters" @removeFilter="removeFilter" />
    <div class="input-loader border">
      <input
        id="search"
        v-model="search.query"
        placeholder="Aretha Franklin"
        type="text"
        @keyup.backspace="removeLastFilter"
      />
      <div class="_loader">
        <Loader />
      </div>
    </div>
  </div>
</template>

<script setup>
import Filters from "../Search/Filters.vue";
import Loader from "../shared/Loader.vue";
import useSearchStore from "../../stores/gsearch";

const search = useSearchStore();

function removeFilter(filter) {
  search.removeFilter(filter);
}

let counter = 0;

function removeLastFilter() {
  if (search.query === "") {
    counter++;

    if (counter > 0) {
      search.removeLastFilter();
    }
  } else {
    counter = 0;
  }
}
</script>

<style lang="scss">
.gsearch-input {
  margin-top: $small;
  padding: 0 $small;
  display: flex;

  .input-loader {
    width: 100%;
    border-radius: 0.4rem;
    position: relative;

    ._loader {
      position: absolute;
      top: -0.25rem;
      right: 2rem;
    }

    input {
      display: flex;
      align-items: center;
      width: 100%;
      border: none;
      line-height: 2rem;
      background-color: transparent;
      color: rgb(255, 255, 255);
      font-size: 1rem;
      outline: none;
      transition: all 0.5s ease;
      padding-left: 0.75rem;

      &:focus {
        transition: all 0.5s ease;
        color: rgb(255, 255, 255);
        outline: none;

        &::placeholder {
          display: none;
        }
      }
    }
  }
}
</style>
