<template>
  <div class="morexx">
    <button
      @click.prevent="loader()"
      :class="{
        load_disabled: !can_load_more,
      }"
    >
      <div class="text">Load More</div>
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  loader: () => void;
  can_load_more: boolean;
}>();
</script>

<style lang="scss">
.morexx {
  display: grid;
  place-items: center;
  margin-top: $small;
  background-color: red;

  button {
    padding: 0 1rem !important;
    width: calc(100% + 2rem);
    border-radius: 0;
    height: 3rem;
    background: $darkestblue;
  }
}
</style>
