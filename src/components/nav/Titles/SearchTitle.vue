<template>
  <div class="nav-search-input">
    <SearchInput :on_nav="true" />
    <TabsWrapper
      :tabs="tabs"
      :currentTab="($route.params.page as string)"
      @switchTab="(tab: string) => {
        $router.push({ name: Routes.search, params: { page: tab } });
        search.switchTab(tab);
      }"
    />
  </div>
</template>

<script setup lang="ts">
import TabsWrapper from "@/components/RightSideBar/Search/TabsWrapper.vue";
import SearchInput from "@/components/RightSideBar/SearchInput.vue";
import { Routes } from "@/router/routes";

import useSearchStore from "@/stores/search";
const search = useSearchStore();

const tabs = ["tracks", "albums", "artists"];
</script>

<style lang="scss">
.nav-search-input {
  align-items: center;
  display: grid;
  grid-template-columns: 1fr max-content;
  gap: 1rem;

  #right-tabs {
    display: grid;
    align-items: center;
  }

  .tabheaders {
    height: 2.25rem;
    margin: 0;
  }
}
</style>
