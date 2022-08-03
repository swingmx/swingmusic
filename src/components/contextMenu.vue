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
    <div
      class="context-item"
      v-for="option in context.options"
      :key="option.label"
      :class="[{ critical: option.critical }, option.type]"
      @click="option.action()"
    >
      <div class="icon image" :class="option.icon"></div>
      <div class="label ellip cap-first">{{ option.label }}</div>
      <div class="more image" v-if="option.children"></div>
      <div class="children rounded shadow-sm" v-if="option.children">
        <div
          class="context-item"
          v-for="child in option.children"
          :key="child.label"
          :class="[{ critical: child.critical }, child.type]"
          @click="child.action()"
        >
          <div class="label ellip cap-first">
            {{ child.label }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import useContextStore from "../stores/context";

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

  .context-item {
    width: 100%;
    display: flex;
    align-items: center;
    cursor: default;
    padding: $small;
    position: relative;

    .more {
      height: 1.5rem;
      width: 1.5rem;
      position: absolute;
      right: 0;
      background-image: url("../assets/icons/expand.svg");
    }

    .children {
      position: absolute;
      right: -13rem;
      width: 13rem;
      top: -0.5rem;
      max-height: 23.5rem;

      padding: $small 0 !important;
      background-color: $context;
      transform: scale(0);
      transform-origin: top left;
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
        transition: transform 0.1s ease-in-out;
      }
    }
  }

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
