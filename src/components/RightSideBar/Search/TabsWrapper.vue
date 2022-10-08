<template>
  <div id="right-tabs" class="rounded">
    <div class="tab-buttons-wrapper">
      <div class="tabheaders rounded-sm no-scroll">
        <div
          class="tab"
          v-for="tab in tabs"
          :key="tab"
          @click="switchTab(tab)"
          :class="{ activetab: tab === currentTab }"
        >
          {{ tab }}
        </div>
      </div>
    </div>

    <div id="tab-content" v-auto-animate>
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  tabs: string[];
  currentTab: string;
}>();

const emit = defineEmits<{
  (e: "switchTab", tab: string): void;
}>();

function switchTab(tab: string) {
  emit("switchTab", tab);
}
</script>

<style lang="scss">
#right-tabs {
  height: 100%;
  display: grid;
  grid-template-rows: min-content 1fr;

  .tab-buttons-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  #tab-content {
    height: 100%;
    overflow: scroll;
    overflow-x: hidden;
    padding-bottom: 1rem;
  }
}
</style>
