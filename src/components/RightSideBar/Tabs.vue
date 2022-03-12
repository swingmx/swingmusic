<template>
  <div class="tabs">
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

<script setup>
import useTabStore from "../../stores/tabs";

const tabs = useTabStore();
</script>

<style lang="scss">
.tabs {
  padding: $small;
  border-left: 1px solid $gray;

  .cont {
    background-color: $gray;
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
      background-color: $gray3;
    }
  }

  .active_tab {
    border-radius: $small;
    display: flex;
    justify-content: center;
    width: 4rem;

    .t-item {
      background-color: transparent;
    }

    background-image: linear-gradient(to right, $blue, $red) !important;
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
