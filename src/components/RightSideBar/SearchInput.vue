<template>
  <div id="gsearch-input">
    <div id="ginner" tabindex="0">
      <div class="icon image"></div>
      <input
        id="search"
        class="rounded"
        v-model="search.query"
        placeholder="Search your library"
        type="text"
        @focus="focusThis()"
        @blur="unfocusThis()"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import useSearchStore from "../../stores/search";

const search = useSearchStore();

function focusThis() {
  document.getElementById("ginner").classList.add("focused");
}

function unfocusThis() {
  document.getElementById("ginner").classList.remove("focused");
}
</script>

<style lang="scss">
#gsearch-input {
  padding: $small;
  display: flex;

  @include tablet-landscape {
    display: none;
  }

  #ginner {
    width: 100%;
    border-radius: 0.4rem;
    position: relative;
    display: flex;
    gap: $small;
    background-color: $gray4;
    height: 2.25rem;

    .icon {
      width: 2rem;
      background-image: url("../../assets/icons/search.svg");
      background-size: 1.5rem;
      margin-left: $smaller;
    }

    input {
      display: flex;
      align-items: center;
      width: 100%;
      border: none;
      line-height: 2.25rem;
      color: inherit;
      font-size: 1rem;
      background-color: transparent;
      outline: 2px solid transparent;
    }
  }

  .focused {
    outline: solid $accent;
  }
}
</style>
