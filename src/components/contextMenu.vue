<template>
  <div
    class="context-menu rounded shadow-lg"
    :class="[
      { 'context-menu-visible': context.visible },
      { 'context-normalizedX': context.normalizedX },
      {
        'context-normalizedY': context.normalizedY,
      },
      {
        'context-many-kids': context.hasManyChildren(),
      },
    ]"
    id="context-menu"
    :style="{
      left: context.x + 'px',
      top: context.y + 'px',
    }"
  >
    <ContextItem
      class="context-item"
      v-for="option in context.options"
      :key="option.label"
      :class="[{ critical: option.critical }, option.type]"
      :option="option"
      @click="option.action()"
    />
  </div>
</template>

<script setup lang="ts">
import useContextStore from "../stores/context";
import ContextItem from "./Contextmenu/ContextItem.vue";

const context = useContextStore();
</script>

<style lang="scss">
.context-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 12rem;
  z-index: 10000 !important;
  transform: scale(0);

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

.context-menu-visible {
  transform: scale(1);
}

.context-normalizedX {
  .more {
    transform: rotate(180deg);
  }

  .context-item > .children {
    left: -13rem;
    transform-origin: center right;
  }
}

.context-normalizedY {
  .context-item > .children {
    transform-origin: bottom right;
    top: -0.5rem;
  }
}

.context-many-kids {
  .context-item > .children {
    overflow-y: auto;
  }
}
</style>
