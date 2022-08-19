<template>
  <div id="gsearch-input" class="rounded">
    <div
      id="ginner"
      tabindex="0"
      class="bg-primary rounded"
    >
      <input
        id="globalsearch"
        v-model="search.query"
        placeholder="Search your library"
        type="search"
      />
      <SearchSvg />
    </div>
    <div class="buttons rounded bg-primary">
      <button @click="tabs.switchToQueue"><QueueSvg /></button>
      <button @click="tabs.switchToSearch"><SearchSvg /></button>
    </div>
  </div>
</template>

<script setup lang="ts">
import QueueSvg from "../../assets/icons/queue.svg";
import SearchSvg from "../../assets/icons/search.svg";
import useSearchStore from "../../stores/search";
import useTabStore from "../../stores/tabs";

const search = useSearchStore();
const tabs = useTabStore();
</script>

<style lang="scss">
#gsearch-input {
  display: grid;
  grid-template-columns: 1fr 7rem;
  gap: 1rem;

  .buttons {
    display: grid;
    grid-auto-flow: column;
    overflow: hidden;

    button {
      padding: 0 $small;
      height: 100%;
      border-radius: 0;
    }
  }

  #ginner {
    width: 100%;
    display: flex;
    align-items: center;
    gap: $smaller;
    padding: 0 1rem;

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
