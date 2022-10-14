<template>
  <div
    v-show="context.visible"
    class="context-menu rounded shadow-lg no-select"
    ref="contextMenu"
    id="context-menu"
  >
    <ContextItem
      class="context-item"
      v-for="option in context.options"
      :key="option.label"
      :class="[{ critical: option.critical }, option.type]"
      :option="option"
      :childrenShowMode="settings.contextChildrenShowMode"
      @hideContextMenu="context.hideContextMenu()"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { onClickOutside } from "@vueuse/core";

import useContextStore from "../stores/context";
import useSettingsStore from "../stores/settings";

import ContextItem from "./Contextmenu/ContextItem.vue";

const context = useContextStore();
const settings = useSettingsStore();
const contextMenu = ref<HTMLElement>();

let clickCount = 0;

onClickOutside(contextMenu, (e) => {
  if (!context.visible) {
    clickCount = 0;
    return;
  }
  clickCount++;

  if (context.visible && clickCount == 2) {
    context.hideContextMenu();
    e.stopImmediatePropagation();
    clickCount = 0;
  }
});
</script>

<style lang="scss">
.context-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 12rem;
  z-index: 10000 !important;
  transform: scale(0);
  height: min-content;

  padding: $small 0;
  background: $context;
  transform-origin: top left;
  font-size: 0.875rem;

  .separator {
    height: 1px;
    padding: 0;
  }

  .critical {
    &:hover {
      background-color: $red;
    }
  }
}
</style>
