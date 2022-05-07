<template>
  <div class="f-container rounded" :class="{ no_f: !props.folders.length }">
    <div id="f-items" v-if="props.folders.length">
      <FolderItem
        v-for="folder in props.folders"
        :key="folder"
        :folder="folder"
      />
    </div>
  </div>
</template>

<script setup>
import FolderItem from "./FolderItem.vue";

const props = defineProps({
  folders: {
    type: Array,
    required: true,
  },
});
</script>

<style lang="scss">

.no_f {
  display: none;
}

#f-items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr));
  gap: $medium;
  border-bottom: 1px solid $gray3;
  padding-bottom: .55rem;
}
</style>
