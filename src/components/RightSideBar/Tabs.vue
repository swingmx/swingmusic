<template>
  <div class="tabs" id="tabs">
    <div class="cont rounded">
      <div
        v-for="tab in tabs.tabs"
        @click="tabs.changeTab(tab)"
        :key="tab"
        class="container"
        :class="{ active_tab: tabs.current === tab }"
      >
        <div class="image t-item" :class="`${tab}`"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import useTabStore from "../../stores/tabs";

const tabs = useTabStore();
</script>

<style lang="scss">
.tabs {
  grid-area: tabs;
  height: 100%;

  .cont {
    background-color: $black;
    display: flex;
    gap: $small;
    height: 100%;
    align-items: center;
    padding-left: $small;
  }

  .t-item {
    float: right;
    width: 2.25rem;
    height: 2.25rem;
    background-size: 1.5rem;
    border-radius: $small;
    transition: all 0.25s;
    width: 4rem;

    &:hover {
      background-color: $gray5;
    }
  }

  .active_tab {
    border-radius: $small;
    display: flex;
    justify-content: center;
    width: 4rem;
    background-color: $accent;

    .t-item {
      background-color: transparent;
    }
  }

  .search {
    background-image: url("../../assets/icons/search.svg");
  }

  .queue {
    background-image: url("../../assets/icons/queue.svg");
  }

  .home {
    background-image: url("../../assets/icons/home.svg");
  }
}
</style>
