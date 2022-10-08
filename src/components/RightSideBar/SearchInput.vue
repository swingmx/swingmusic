<template>
  <div class="gsearch-input">
    <div id="ginner" tabindex="0" ref="inputRef">
      <button
        v-auto-animate
        :title="
          tabs.current === tabs.tabs.search ? 'back to queue' : 'go to search'
        "
        @click.prevent="handleButton"
        :class="{ no_bg: on_nav }"
      >
        <SearchSvg v-if="on_nav || tabs.current === tabs.tabs.queue" />
        <BackSvg v-else-if="tabs.current === tabs.tabs.search" />
      </button>
      <input
        id="globalsearch"
        v-model.trim="search.query"
        placeholder="Start typing to search"
        type="text"
        autocomplete="off"
        @blur.prevent="removeFocusedClass"
        @focus.prevent="addFocusedClass"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import useTabStore from "@/stores/tabs";
import useSearchStore from "@/stores/search";

import BackSvg from "@/assets/icons/arrow.svg";
import SearchSvg from "@/assets/icons/search.svg";

const props = defineProps<{
  on_nav?: boolean;
}>();

const tabs = useTabStore();
const search = useSearchStore();

// HANDLE FOCUS
const inputRef = ref<HTMLElement>();
function addFocusedClass() {
  inputRef.value?.classList.add("search-focused");
}

function removeFocusedClass() {
  inputRef.value?.classList.remove("search-focused");
}

// @end

function handleButton() {
  if (props.on_nav) return;

  if (tabs.current === tabs.tabs.search) {
    tabs.switchToQueue();
  } else {
    tabs.switchToSearch();
  }
}
</script>

<style lang="scss">
.gsearch-input {
  display: grid;
  grid-template-columns: 1fr max-content;
  border-radius: 3rem;

  #ginner {
    width: 100%;
    display: flex;
    align-items: center;
    gap: $small;
    border-radius: 3rem;
    outline: solid 1px $gray3;

    button {
      background: transparent;
      width: 3rem;
      padding: 0;
      border-radius: 3rem;
      height: 100%;
      cursor: pointer;

      &:hover {
        transition: all 0.2s ease;
        background-color: $gray2;
      }
    }

    button.no_bg {
      pointer-events: none;
    }

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
  outline: solid $darkblue !important;
}
</style>
