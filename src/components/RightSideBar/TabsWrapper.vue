<template>
  <div id="right-tabs">
    <div id="tabheaders">
      <div
        class="tab rounded"
        v-for="slot in $slots.default()"
        :key="slot.key"
        @click="currentTab = slot.props.name"
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
import { ref, provide } from "vue";

const currentTab = ref("Tracks");
provide("currentTab", currentTab);
</script>

<style lang="scss">
#right-tabs {
  height: 100%;
  margin-right: $small;
  display: grid;
  grid-template-rows: min-content 1fr;

  #tabheaders {
    border: solid 1px rgb(0, 68, 255);
    display: flex;
    gap: $small;
    margin: $small 0;

    .tab {
      background-color: $gray3;
      padding: $small;
      text-transform: capitalize;
    }
  }

  #tab-content {
    height: 100%;
    overflow: auto;
    border-radius: $small;
    background-color: $gray;
    // overflow: hidden;
  }
}
</style>
