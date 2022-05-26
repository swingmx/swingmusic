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
          <UpNext />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Search from "./Search/Main.vue";
import UpNext from "./Queue.vue";
import Main from "./Home/Main.vue";
import useTabStore from "../../stores/tabs";
// import Search from "./Searchh.vue";
const DashBoard = Main;
const tabs = useTabStore();
</script>

<style lang="scss">
.r-sidebar {
  width: 29em;
  background-color: rgba(4, 12, 34, 0.103);
  padding: 0 0 0 $small;

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

    .tab-keys {
      display: none;
      width: 3rem;
      right: 0;
      height: 100%;
      position: absolute;
      grid-area: tabs;
      border-radius: 0;
      overflow: hidden;
      border-left: solid 1px $gray;
    }
  }
}
</style>
