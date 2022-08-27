<template>
  <div class="context-item">
    <div class="icon image" :class="option.icon"></div>
    <div class="label ellip">{{ option.label }}</div>
    <div class="more image" v-if="option.children"></div>
    <div class="children rounded shadow-sm" v-if="option.children">
      <div
        class="context-item"
        v-for="child in option.children"
        :key="child.label"
        :class="[{ critical: child.critical }, child.type]"
        @click="child.action()"
      >
        <div class="label ellip">
          {{ child.label }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Option } from "@/interfaces";

defineProps<{
  option: Option;
}>();
</script>

<style lang="scss">
.context-item {
  width: 100%;
  display: flex;
  align-items: center;
  cursor: default;
  padding: 0.4rem 1rem;
  position: relative;

  .more {
    height: 1.5rem;
    width: 1.5rem;
    position: absolute;
    right: $small;
    background-image: url("../assets/icons/expand.svg");
  }

  .children {
    position: absolute;
    right: -13rem;
    width: 13rem;
    top: -0.5rem;
    max-height: 23.5rem;

    background-color: $context;
    transform: scale(0);
    transform-origin: top left;
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

    .children {
      transform: scale(1);
      transition: transform 0.1s ease-in-out;
      transition-delay: 0.3s;
    }
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

  .add_to_queue {
    background-image: url("../../assets/icons/add_to_queue.svg");
  }

  .heart {
    background-image: url("../../assets/icons/heart.svg");
  }
}
</style>
