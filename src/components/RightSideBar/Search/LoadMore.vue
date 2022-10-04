<template>
  <div class="morexx">
    <button class="btn" @click.prevent="loader()">
      <div class="text">Load More</div>
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  loader: () => void;
}>();


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
