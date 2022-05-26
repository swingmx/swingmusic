<template>
  <div id="right-tabs">
    <div id="tabheaders">
      <div
        class="tab rounded"
        v-for="slot in $slots.default()"
        :key="slot.key"
        @click="s.changeTab(slot.props.name)"
        :class="{ activetab: slot.props.name === s.currentTab }"
      >
        {{ slot.props.name }}
      </div>
    </div>
    <div id="tab-content">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import useSearchStore from "@/stores/search";

const s = useSearchStore();
</script>

<style lang="scss">
#right-tabs {
  height: 100%;
  margin-right: $small;
  display: grid;
  grid-template-rows: min-content 1fr;

  #tabheaders {
    display: flex;
    gap: $small;
    margin: $small 0;

    .tab {
      background-color: $gray3;
      padding: $small;
      text-transform: capitalize;
      cursor: pointer;
      display: flex;
      justify-content: center;
      transition: all 0.3s ease;
      width: 4rem;
    }

    .activetab {
      background-color: $accent;
      width: 6rem;
      transition: all 0.3s ease;
    }
  }

  #tab-content {
    height: 100%;
    overflow: auto;
    overflow-x: hidden;
    border-radius: $small;
    background-color: $gray;
    // overflow: hidden;
  }
}
</style>
