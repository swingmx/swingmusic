<template>
  <div
    class="r-sidebar"
    :style="{
      marginBottom: !settings.use_alt_np ? '-1rem' : '',
    }"
  >
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
import useSettingsStore from "@/stores/settings";

const tabs = useTabStore();
const settings = useSettingsStore();
</script>

<style lang="scss">
.r-sidebar {
  width: 100%;

  .grid {
    display: flex;
    position: relative;
    height: 100%;

    .r-content {
      grid-area: content;
      overflow: hidden;
      width: 100%;

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
