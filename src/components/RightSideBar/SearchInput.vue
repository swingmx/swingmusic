<template>
  <div id="gsearch-input">
    <div id="ginner" tabindex="0" class="bg-primary rounded-sm">
      <input
        id="globalsearch"
        v-model="search.query"
        placeholder="Search your library"
        type="search"
        @blur.prevent="removeFocusedClass"
        @focus.prevent="addFocusedClass"
      />
      <SearchSvg />
    </div>
    <div class="buttons rounded-sm bg-primary">
      <button
        @click="tabs.switchToQueue"
        v-if="tabs.current !== tabs.tabs.queue"
      >
        <QueueSvg />
      </button>
      <button
        @click="tabs.switchToSearch"
        v-if="tabs.current !== tabs.tabs.search"
      >
        <SearchSvg />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import QueueSvg from "../../assets/icons/queue.svg";
import SearchSvg from "../../assets/icons/search.svg";
import useSearchStore from "../../stores/search";
import useTabStore from "../../stores/tabs";

const search = useSearchStore();
const tabs = useTabStore();
let classList: DOMTokenList | undefined;

onMounted(() => {
  classList = document.getElementById("ginner")?.classList;
});

function addFocusedClass() {
  classList?.add("search-focused");
}

function removeFocusedClass() {
  classList?.remove("search-focused");
}
</script>

<style lang="scss">
#gsearch-input {
  display: grid;
  grid-template-columns: 1fr max-content;
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
