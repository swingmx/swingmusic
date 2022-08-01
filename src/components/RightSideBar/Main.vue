<template>
  <div class="r-sidebar">
    <div class="grid">
      <div class="r-content">
        <div class="r-dash" v-show="tabs.current === tabs.tabs.home">
          <DashBoard />
        </div>
        <div class="r-search" v-show="tabs.current === tabs.tabs.search">
          <Search />
        </div>
        <div class="r-queue" v-show="tabs.current === tabs.tabs.queue">
          <Queue />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Search from "./Search/Main.vue";
import Queue from "./Queue.vue";
import DashBoard from "./Home/Main.vue";
import useTabStore from "../../stores/tabs";

const tabs = useTabStore();
</script>

<style lang="scss">
.r-sidebar {


  @include phone-only {
    display: none;
  }

  @include tablet-landscape {
    display: none;
  }

  .grid {
    height: 100%;
    display: flex;
    position: relative;

    .r-content {
      grid-area: content;
      width: 29rem;

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
  }
}
</style>
