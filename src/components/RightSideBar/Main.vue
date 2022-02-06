<template>
  <div class="r-sidebar">
    <div class="grid">
      <div class="r-content">
        <div class="r-dash" v-show="current_tab == tabs.home">
          <DashBoard />
        </div>
        <div class="r-search" v-show="current_tab == tabs.search">
          <Search />
        </div>

        <div class="r-queue" v-show="current_tab == tabs.queue">
          <UpNext />
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

const tabs = {
  home: "home",
  search: "search",
  queue: "queue",
};

const current_tab = ref(tabs.queue);

function changeTab(tab) {
  current_tab.value = tab;
}
</script>

<style lang="scss">
.r-sidebar {
  width: 34.5em;
  margin: $small 0 $small 0;
  
  @include phone-only {
    display: none;
  }

  // @include tablet-landscape {
  //   width: 3rem;
  // }

  .grid {
    height: 100%;
    display: flex;
    position: relative;

    .r-content {
      grid-area: content;
      width: 31rem;

      // @include tablet-landscape {
      //   display: none;
      // }

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
      right: 0;
      height: 100%;
      position: absolute;
      grid-area: tabs;
      padding: $small;
      border-radius: $small 0 0 $small;
    }
  }
}
</style>
