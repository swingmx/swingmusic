<template>
  <div class="morexx">
    <button @click="loadMore" class="btn">
      <div class="text">Load More</div>
    </button>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  (e: "loadMore"): void;
}>();

function loadMore() {
  emit("loadMore");
}
</script>

<style lang="scss">
.morexx {
  display: grid;
  place-items: center;
  margin-top: $small;

  button {
    padding: 0 1rem !important;
  }
}
</style>
