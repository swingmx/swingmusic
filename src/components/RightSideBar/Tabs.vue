<template>
  <div class="tabs">
    <div class="cont rounded">
      <div
        v-for="tab in tabs.tabs"
        @click="tabs.changeTab(tab)"
        :key="tab"
        class="image t-item"
        :class="({ active_tab: tabs.current === tab }, `${tab}`)"
      ></div>
    </div>
  </div>
</template>

<script setup>
import useTabStore from "../../stores/tabs";

const tabs = useTabStore()
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
    background-color: $gray4;

    &:hover {
      background-color: rgba(128, 128, 128, 0.281);
    }
  }

  .active_tab {
    border: solid;
    background-color: rgba(17, 123, 223, 0.192);
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
