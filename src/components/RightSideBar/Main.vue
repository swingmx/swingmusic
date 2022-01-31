<template>
  <div class="r-sidebar">
    <div class="grid">
      <div class="r-content border rounded">
        <div class="r-dash" v-if="current_tab == tabs.home">
          <DashBoard/>
        </div>
        <div class="r-search" v-if="current_tab == tabs.search">
          <Search
            v-model:search="search"
            @expandSearch="expandSearch"
            @collapseSearch="collapseSearch"
          />
        </div>

        <div class="r-queue" v-if="current_tab == tabs.queue">
          <UpNext v-model:up_next="up_next" @expandQueue="expandQueue" />
        </div>
      </div>
      <div class="tab-keys card-dark border">
        <Tabs :current_tab="current_tab" :tabs="tabs" @changeTab="changeTab" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Search from "../Search.vue";
import UpNext from "./Queue.vue";
import Tabs from "./Tabs.vue";
import Main from "./Home/Main.vue";

const DashBoard = Main;

let up_next = ref(true);
let search = ref(false);

const expandQueue = () => {
  up_next.value = !up_next.value;
};

const expandSearch = () => {
  search.value = true;
};

const collapseSearch = () => {
  search.value = false;
};

const tabs = {
  home: "home",
  search: "search",
  queue: "queue",
};

const current_tab = ref(tabs.search);

function changeTab(tab) {
  current_tab.value = tab;
}
</script>

<style lang="scss">
.r-sidebar {
  width: 34em;

  .grid {
    height: 100%;
    display: grid;
    grid-template-areas: "content tabs";

    .r-content {
      grid-area: content;
      width: 100%;
      overflow: hidden;
      margin: $small $small $small 0;

      .r-search {
        height: 100%;
      }

      .r-dash {
        height: 100%;
      }

      .r-queue {
        height: 100%;
      }
    }

    .tab-keys {
      grid-area: tabs;
      width: 3rem;
      padding: $small;
      margin-left: $small;
    }
  }
}
</style>
