<template>
  <div
    class="context-item"
    @mouseenter="
      option.children &&
        childrenShowMode === contextChildrenShowMode.hover &&
        showChildren()
    "
    @mouseleave="
      option.children &&
        childrenShowMode === contextChildrenShowMode.hover &&
        hideChildren()
    "
    @click="runAction"
    ref="parentRef"
  >
    <div class="icon image" :class="option.icon"></div>
    <div class="label ellip">{{ option.label }}</div>
    <div class="more image" v-if="option.children"></div>
    <div
      class="children rounded shadow-sm"
      v-if="option.children"
      ref="childRef"
    >
      <div
        class="context-item"
        v-for="child in option.children"
        :key="child.label"
        :class="[{ critical: child.critical }, child.type]"
        @click="child.action && runChildAction(child.action)"
      >
        <div class="label ellip">
          {{ child.label }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { createPopper, Instance } from "@popperjs/core";
import { ref } from "vue";

import { contextChildrenShowMode } from "@/composables/enums";
import { Option } from "@/interfaces";

const props = defineProps<{
  option: Option;
  childrenShowMode: contextChildrenShowMode;
}>();

const emit = defineEmits<{
  (event: "hideContextMenu"): void;
}>();

const parentRef = ref<HTMLElement>();
const childRef = ref<HTMLElement>();
const childrenShown = ref(false);

let popperInstance: Instance | null = null;

function showChildren() {
  if (childrenShown.value) {
    childrenShown.value = false;
    return;
  }

  popperInstance = createPopper(
    parentRef.value as HTMLElement,
    childRef.value as HTMLElement,
    {
      placement: "right-start",
      modifiers: [
        {
          name: "offset",
          options: {
            offset: [-5, -2],
          },
        },
      ],
    }
  );
  childRef.value ? (childRef.value.style.visibility = "visible") : null;
  childrenShown.value = true;
}

function hideChildren() {
  childRef.value ? (childRef.value.style.visibility = "hidden") : null;
  popperInstance?.destroy();
  childrenShown.value = false;
}

function hideContextMenu() {
  if (props.option.children) return;
  emit("hideContextMenu");
}

function runAction() {
  if (props.option.children) {
    if (childrenShown.value) {
      hideChildren();
      return;
    }

    showChildren();
    return;
  }

  props.option.action && props.option.action();
  hideContextMenu();
}

function runChildAction(action: () => void) {
  action();
  emit("hideContextMenu");
}
</script>

<style lang="scss">
.context-item {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0.4rem 1rem;
  position: relative;

  .more {
    height: 1.5rem;
    width: 1.5rem;
    position: absolute;
    right: $small;
    background-image: url("../../assets/icons/expand.svg");
  }

  .children {
    position: absolute;
    width: 13rem;

    background-color: $context;
    transform: scale(0);
    padding: $small 0;

    .context-item {
      padding: $small 1rem;
    }

    .separator {
      padding: 0;
    }
  }

  &:hover {
    background: $darkestblue;
  }

  .children {
    transform: scale(0);
    overflow: hidden;
    max-height: calc(100vh - 10rem);
  }

  .icon {
    height: 1.25rem;
    width: 1.25rem;
    margin-right: $small;
  }

  .label {
    width: 9rem;
  }

  .folder {
    background-image: url("../../assets/icons/folder.svg");
  }

  .artist {
    background-image: url("../../assets/icons/artist.svg");
  }

  .album {
    background-image: url("../../assets/icons/album.svg");
  }

  .delete {
    background-image: url("../../assets/icons/delete.svg");
  }

  .plus {
    background-image: url("../../assets/icons/plus.svg");
  }

  .play_next {
    background-image: url("../../assets/icons/add_to_queue.svg");
  }

  .add_to_queue {
    background-image: url("../../assets/icons/add-to-queue.svg");
    transform: scale(0.8); // reason: icon is not from same source as other
  }

  .heart {
    background-image: url("../../assets/icons/heart.svg");
  }
}
</style>
