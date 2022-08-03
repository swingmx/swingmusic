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
  grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr));
  gap: $medium;
  padding: $small;
  background-color: $gray5;
}
</style>
