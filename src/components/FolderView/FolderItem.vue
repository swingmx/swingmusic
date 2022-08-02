<template>
  <router-link :to="{ name: 'FolderView', params: { path: folder.path } }">
    <div class="f-item">
      <div class="icon">
        <FolderSvg v-if="!folder.is_sym" />
        <SymLinkSvg v-if="folder.is_sym" />
      </div>
      <div class="info">
        <div class="f-item-text ellip">{{ folder.name }}</div>
        <div class="separator no-border"></div>
        <div class="f-item-count">{{ folder.trackcount }} tracks</div>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { Folder } from "@/interfaces";
import FolderSvg from "../../assets/icons/folder.svg";
import SymLinkSvg from "../../assets/icons/symlink.svg";

defineProps<{
  folder: Folder;
}>();
</script>

<style lang="scss">
.f-container .f-item {
  height: 5rem;
  display: grid;
  grid-template-columns: max-content 1fr;
  padding-right: 1rem;
  align-items: center;
  background-color: $gray3;
  transition: all 0.2s ease;
  border-radius: 0.75rem;

  @include phone-only {
    height: 4rem;
  }

  .icon {
    margin: 0 0.75rem;
  }

  .info {
    .f-item-count {
      font-size: 0.8rem;
      color: rgba(219, 217, 217, 0.63);
    }

    .f-item-text {
      text-align: left;
    }
  }

  &:hover {
    background: #0575e6;
    background: linear-gradient(to top right, #021b79, #0575e6);
    background-size: 105% 105%;
    background-position-x: -$small;

    .f-item-count {
      color: #ffffff;
    }
  }
}
</style>
