<template>
  <div id="right-tabs" class="bg-black rounded">
    <div class="tab-buttons-wrapper">
      <div id="tabheaders" class="rounded noscroll">
        <div
          class="tab cap-first"
          v-for="slot in $slots.default()"
          :key="slot.key"
          @click="s.changeTab(slot.props.name)"
          :class="{ activetab: slot.props.name === s.currentTab }"
        >
          {{ slot.props.name }}
        </div>
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
  display: grid;
  grid-template-rows: min-content 1fr;

  .tab-buttons-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  #tabheaders {
    display: grid;
    grid-template-columns: repeat(5, max-content);
    justify-content: space-around;
    margin: 1rem;
    width: max-content;
    background: linear-gradient(37deg, $gray3, $gray4, $gray3);
    height: 2rem;

    & > * {
      border-left: solid 1px $gray3;
    }

    .tab {
      display: flex;
      align-items: center;
      justify-content: center;

      cursor: pointer;
      transition: all 0.3s ease;
      padding: 0 $small;

      &:first-child {
        border-left: solid 1px transparent;
      }
    }

    .activetab {
      background-color: $darkblue;
      transition: all 0.3s ease;
      border-left: solid 1px transparent;
    }
  }

  #tab-content {
    height: 100%;
    overflow: auto;
    overflow-x: hidden;
    padding-bottom: 1rem;
  }
}
</style>
