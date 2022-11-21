<template>
  <div
    v-show="context.visible"
    class="context-menu rounded shadow-lg no-select"
    ref="contextMenuRef"
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

import useContextStore from "@/stores/context";
import useSettingsStore from "@/stores/settings";

import ContextItem from "./Contextmenu/ContextItem.vue";

const context = useContextStore();
const settings = useSettingsStore();
const contextMenuRef = ref<HTMLElement>();

// let clickCount = 0;

// onClickOutside(
//   contextMenuRef,
//   (e) => {
//     console.log(clickCount);

//     if (!context.visible) {
//       // clickCount = 0;
//       return;
//     }

//     clickCount++;

//     if (context.visible && clickCount === 1) {
//       context.hideContextMenu();
//       e.stopImmediatePropagation();
//       clickCount = 0;
//     }
//   },
//   {
//     capture: false,
//   }
// );

let watcher: any = null;

context.$subscribe((mutation, state) => {
  // let watchers = [];
  // console.log("watchers count: " + watchers.length)
  // let wat: any = () => {};

  if (state.visible) {
    setTimeout(() => {
      if (watcher !== null) {
        watcher();
      }
      watcher = onClickOutside(
        contextMenuRef,
        (e) => {
          e.stopImmediatePropagation();
          console.log("clicked outside ref");
          context.hideContextMenu();
        },
        {
          capture: false,
        }
      );
    }, 200);
    return;
  }

  if (watcher !== null) {
    watcher();
  }

  // wat();
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
