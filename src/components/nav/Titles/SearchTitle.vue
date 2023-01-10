<template>
  <div class="nav-search-input">
    <SearchInput :on_nav="true" />
    <div class="buttons-area">
      <Tabs
        :tabs="tabs"
        :currentTab="($route.params.page as string)"
        @switchTab="(tab: string) => {
        $router.replace({ name: Routes.search, params: { page: tab }, query: {
          q: search.query,
        } });
        search.switchTab(tab);
      }"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Routes } from "@/router/routes";

import useSearchStore from "@/stores/search";
import Tabs from "@/components/RightSideBar/Search/TabsWrapper.vue";
import SearchInput from "@/components/RightSideBar/SearchInput.vue";

const search = useSearchStore();
const tabs = ["tracks", "albums", "artists"];
</script>

<style lang="scss">
.nav-search-input {
  align-items: center;
  display: grid;
  grid-template-columns: 1fr max-content;
  gap: 1rem;
  
  .buttons-area {
    position: relative;
    height: 100%;
    width: 12rem;
  }

  #right-tabs {
    width: max-content;
    height: max-content;

    .tabheaders {
      height: 38px;
    }
  }

  .tabheaders {
    height: 2.25rem;
    margin: 0;
  }
}
</style>
