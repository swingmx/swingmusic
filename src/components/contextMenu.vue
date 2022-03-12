<template>
  <div
    class="context-menu rounded"
    :class="{ 'context-menu-visible': context.visible }"
    v-show="context.visible"
    :style="{
      left: context.x + 'px',
      top: context.y + 'px',
    }"
  >
    <div class="context-item" v-for="option in options" :key="option.label">
      <div class="icon image" :class="option.icon"></div>
      <div class="label ellip" @click="option.action">{{ option.label }}</div>
    </div>
  </div>
</template>

<script setup>
import useContextStore from "@/stores/context.js";

const context = useContextStore();

// const props = defineProps({
//   context: {
//     type: Object,
//     required: true,
//   },
// });

const options = [
  {
    label: "Item 1 and another one of my long stories",
    icon: "folder",
    action: () => {
      console.log("Item 1 clicked");
    },
  },
  {
    label: "Item 2",
    icon: "folder",

    action: () => {
      console.log("Item 2 clicked");
    },
  },
  {
    label: "Item 3",
    icon: "folder",
    action: () => {
      console.log("Item 3 clicked");
    },
  },
  {
    label: "Item 4",
    icon: "folder",

    action: () => {
      console.log("Item 4 clicked");
    },
  },
  {
    label: "Item 5",
    icon: "folder",

    action: () => {
      console.log("Item 5 clicked");
    },
  },
];

</script>

<style lang="scss">
.context-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 14rem;
  height: min-content;
  padding: $small;
  background: $gray;
  z-index: 100000 !important;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  .context-item {
    width: 100%;
    height: 3rem;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    cursor: pointer;
    padding: 0 $small;
    border-radius: $small;
    transition: background 0.2s ease-in-out;

    .icon {
      height: 1.25rem;
      width: 1.25rem;
      margin-right: $small;
    }

    .label {
      width: 10rem;
    }

    .folder {
      background-image: url("../assets/icons/folder.svg");
    }

    &:hover {
      background: #234ece;
    }
  }
}

// .visible {
//     display: unset;
// }
</style>
