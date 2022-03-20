<template>
  <!-- v-show="context.visible" -->
  <div
    class="context-menu rounded shadow-lg"
    :class="[
      { 'context-menu-visible': context.visible },
      { 'context-normalizedX': context.normalizedX },
      {
        'context-normalizedY': context.normalizedY && context.hasManyChildren(),
      },
    ]"
    :style="{
      left: context.x + 'px',
      top: context.y + 'px',
    }"
  >
    <div
      class="context-item"
      v-for="option in context.options"
      :key="option.label"
      :class="[{ critical: option.critical }, option.type]"
      @click="option.action"
    >
      <div class="icon image" :class="option.icon"></div>
      <div class="label ellip">{{ option.label }}</div>
      <div class="more image" v-if="option.children"></div>
      <div class="children rounded shadow-sm" v-if="option.children">
        <div class="context-item" v-for="child in option.children" :key="child">
          <div class="label ellip" @click="child.action()">
            {{ child.label }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import useContextStore from "../stores/context";

const context = useContextStore();
</script>

<style lang="scss">
.context-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 12rem;
  height: min-content;
  z-index: 100000 !important;
  transform: scale(0);

  padding: $small;
  background: $gray3;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transform-origin: top left;
  font-size: 0.875rem;

  .context-item {
    width: 100%;
    height: 2.25rem;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    cursor: default;
    padding: 0 $small;
    border-radius: $small;
    color: rgb(255, 255, 255);
    position: relative;

    .more {
      height: 1.5rem;
      width: 1.5rem;
      position: absolute;
      right: 0;
      background-image: url("../assets/icons/more.svg");
    }

    .children {
      position: absolute;
      right: -13rem;
      width: 13rem;

      padding: $small;
      background: $gray3;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      transform: scale(0);
      transform-origin: left;
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
      background-image: url("../assets/icons/folder.svg");
    }

    .artist {
      background-image: url("../assets/icons/artist.svg");
    }

    .album {
      background-image: url("../assets/icons/album.svg");
    }

    .delete {
      background-image: url("../assets/icons/delete.svg");
    }

    .plus {
      background-image: url("../assets/icons/plus.svg");
    }

    .add_to_queue {
      background-image: url("../assets/icons/add_to_queue.svg");
    }

    .heart {
      background-image: url("../assets/icons/heart.svg");
    }

    &:hover {
      background: #234ece;

      .children {
        transform: scale(1);
        transition: transform 0.2s ease-in-out;
      }
    }
  }

  .separator {
    height: 1px;
  }

  .critical {
    &:hover {
      background-color: $red;
    }
  }
}

.context-menu-visible {
  transform: scale(1);
  transition: transform 0.2s ease-in-out;
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
    bottom: -0.5rem;
    transform-origin: bottom right;
  }
}
</style>
