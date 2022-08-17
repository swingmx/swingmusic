<template>
  <div
    id="gsearch-input"
    class="bg-black rounded"
    :class="{ 'search-focused': focused }"
  >
    <div id="ginner" tabindex="0">
      <SearchSvg />
      <input
        id="globalsearch"
        v-model="search.query"
        placeholder="Search your library"
        type="search"
        @focus="focused = true"
        @blur="focused = false"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import useSearchStore from "../../stores/search";
import SearchSvg from "../../assets/icons/search.svg";

const search = useSearchStore();
const focused = ref(false);
</script>

<style lang="scss">
#gsearch-input {
  padding: $smaller;

  #ginner {
    width: 100%;
    display: flex;
    align-items: center;
    gap: $smaller;
    margin-left: $small;

    input {
      width: 100%;
      border: none;
      line-height: 2.25rem;
      color: inherit;
      font-size: 1rem;
      background-color: transparent;
      outline: none;
    }
  }
}
.search-focused {
  outline: solid $accent;
}
</style>
