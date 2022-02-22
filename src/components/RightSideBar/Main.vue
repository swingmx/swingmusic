<template>
  <div class="r-sidebar">
    <div class="grid">
      <div class="r-content">
        <div class="r-dash" v-show="current_tab === tabs.home">
          <DashBoard />
        </div>
        <div class="r-search" v-show="current_tab === tabs.search">
          <Search />
        </div>

        <div class="r-queue" v-show="current_tab === tabs.queue">
          <UpNext />
        </div>
      </div>
      <div class="tab-keys border">
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
import perks from "../../composables/perks";

const DashBoard = Main;

const tabs = {
  home: "home",
  search: "search",
  queue: "queue",
};

const default_tab = tabs.home;

const current_tab = ref(default_tab);

function changeTab(tab) {
  new Promise((resolve) => {
    current_tab.value = tab;
    resolve();
    setTimeout(() => {}, 300);
  }).then(() => {
    if (tab === tabs.queue) {
      setTimeout(() => {
        perks.focusCurrent();
      }, 300);
    }
  });
}
</script>

<style lang="scss">
.r-sidebar {
  width: 32em;

  @include phone-only {
    display: none;
  }

  @include tablet-landscape {
    width: 3rem;
  }

  .grid {
    height: 100%;
    display: flex;
    position: relative;

    .r-content {
      grid-area: content;
      width: 29rem;


      @include tablet-landscape {
        display: none;
      }

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
      width: 3rem;
      right: 0;
      height: 100%;
      position: absolute;
      grid-area: tabs;
      // padding: $small 0;
      border-radius: 0;
      overflow: hidden;
    }
  }
}
</style>
