<template>
  <div class="morexx">
    <div @click="loadMore" class="btn circular">
      <div class="text">Load More</div>
    </div>
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

  .btn {
    height: 2.5rem;
    width: 15rem;
    display: grid;
    place-items: center;
    transition: all 0.5s ease;
    background-image: linear-gradient(37deg, $red, $blue);
    cursor: pointer;

    &:hover {
      background-color: $blue !important;
      width: 12rem;
    }
  }
}
</style>
