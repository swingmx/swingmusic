<template>
  <div class="f-container rounded">
    <div id="f-items" class="rounded">
      <FolderItem
        v-for="folder in folders"
        :key="JSON.stringify(folder)"
        :folder="folder"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Folder } from "@/interfaces";
import FolderItem from "./FolderItem.vue";

defineProps<{
  folders: Folder[];
}>();
</script>

<style lang="scss">
#f-items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.75rem;
}

#f-items.list-mode {
  grid-template-columns: 1fr;
  gap: 0;

  .f-item {
    height: 3.25rem;
    border-radius: $small;
    background-color: transparent;
  }

  .f-item:hover {
    background-color: $gray !important;
  }
}
</style>

<!-- TODO: ADD BUTTON TO TOGGLE LIST MODE -->