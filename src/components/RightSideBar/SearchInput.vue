<template>
  <div class="gsearch-input">
    <div id="ginner" tabindex="0" class="bg-primary">
      <button
        :title="
          tabs.current === tabs.tabs.search ? 'back to queue' : 'go to search'
        "
      >
        <SearchSvg
          v-if="on_nav || tabs.current === tabs.tabs.queue"
          @click.prevent="!on_nav && tabs.switchToSearch()"
        />
        <BackSvg
          v-else-if="tabs.current === tabs.tabs.search"
          @click.prevent="tabs.switchToQueue"
        />
      </button>
      <input
        id="globalsearch"
        v-model.trim="search.query"
        placeholder="Search your library"
        type="text"
        autocomplete="off"
        @blur.prevent="removeFocusedClass"
        @focus.prevent="addFocusedClass"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import BackSvg from "@/assets/icons/arrow.svg";
import SearchSvg from "@/assets/icons/search.svg";
import useSearchStore from "@/stores/search";
import useTabStore from "@/stores/tabs";

defineProps<{
  on_nav?: boolean;
}>();

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

    button {
      background: transparent;
      width: 3rem;
      padding: 0;
      border-radius: 3rem;
      cursor: pointer;

      &:hover {
        transition: all 0.2s ease;
        background-color: $gray2;
      }
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
  outline: solid $accent;
}
</style>
