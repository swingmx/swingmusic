<template>
  <div
    class="r-sidebar rounded border"
    :style="{
      marginBottom: !settings.show_alt_np ? '-1rem' : '',
    }"
  >
    <div class="r-content">
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

const tabs = useTabStore();
const settings = useSettingsStore();
</script>

<style lang="scss">
.r-sidebar {
  width: 100%;
  overflow: hidden;

  .r-content {
    width: 100%;
    height: 100%;

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
      grid-template-rows: max-content 1fr;
    }
  }
}
</style>
