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
.f-container {
  padding: 0 0 0 0;
}

.no_f {
  display: none;
}

#f-items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr));
  gap: $medium;
}

.f-container p {
  text-transform: uppercase;
  font-weight: normal;
  color: rgba(255, 255, 255, 0.438);
  margin-bottom: 1rem;
}
</style>
