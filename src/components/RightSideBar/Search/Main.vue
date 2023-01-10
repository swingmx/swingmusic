<template>
  <div class="right-search">
    <TabsWrapper
      :tabs="tabs"
      @switchTab="switchTab"
      :currentTab="currentTab"
      :tabContent="true"
    >
      <Tab :name="currentTab" :isOnSearchPage="isOnSearchPage" />
    </TabsWrapper>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import useSearchStore from "@/stores/search";
import Tab from "./Tab.vue";
import TabsWrapper from "./TabsWrapper.vue";

const search = useSearchStore();
defineProps<{
  isOnSearchPage?: boolean;
}>();

const tabs = ["tracks", "albums", "artists"];

const currentTab = ref("tracks");

function switchTab(tab: string) {
  currentTab.value = tab;
  search.switchTab(tab);
}
</script>

<style lang="scss">
.right-search {
  position: relative;
  overflow: hidden;
  height: 100%;
  width: 100%;
  display: grid;
  grid-template-rows: max-content 1fr;

  .heading {
    padding: $medium;
    border-radius: $small;
    margin-bottom: $small;
    font-size: 2rem;
    color: $white;
  }

  .input {
    display: flex;
    align-items: center;
    position: relative;
  }
}
</style>
