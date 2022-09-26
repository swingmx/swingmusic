<template>
  <div
    class="r-sidebar border"
    :style="{
      marginBottom: !settings.show_alt_np ? '-1rem' : '',
    }"
  >
  <SearchInput />
    <div class="r-content noscroll">
      <div class="r-dash" v-if="tabs.current === tabs.tabs.home">
        <DashBoard />
      </div>
      <div class="r-search" v-if="tabs.current === tabs.tabs.search">
        <Search />
      </div>
      <div class="r-queue" v-if="tabs.current === tabs.tabs.queue">
        <Queue />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Search from "./Search/Main.vue";
import Queue from "./Queue.vue";
import DashBoard from "./Home/Main.vue";
import useTabStore from "../../stores/tabs";
import useSettingsStore from "@/stores/settings";
import SearchInput from "./SearchInput.vue";

const tabs = useTabStore();
const settings = useSettingsStore();
</script>

<style lang="scss">
.r-sidebar {
  width: 100%;
  display: grid;
  grid-template-rows: max-content 1fr;
  background-color: rgb(22, 22, 22);
  padding-bottom: 1rem;
  border-top: none;
  border-bottom: none;

  .gsearch-input {
    height: 2.5rem;
    margin: 1rem;
  }

  .r-content {
    width: 100%;
    height: 100%;
    background-color: $gray;

    .r-search {
      height: 100%;
    }

    .r-dash {
      height: 100%;
    }

    .r-queue {
      height: 100%;
      overflow: hidden;
      display: grid;
      gap: $small;
      grid-template-rows: max-content 1fr;
    }
  }
}
</style>
