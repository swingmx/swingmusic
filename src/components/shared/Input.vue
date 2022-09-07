<template>
  <input
    type="search"
    class="header-input rounded-sm pad-sm"
    placeholder="search here"
    v-model="ref_value"
  />
</template>

<script setup lang="ts">
import { ref, Ref } from "vue";

defineProps<{
  ref_value?: Ref<string> | undefined;
}>();
</script>

<style lang="scss">
.header-input {
  background-color: $gray3;
  outline: none;
  border: none;
  color: inherit;
  font-size: 1rem;
  z-index: 200;

  &:focus {
    outline: solid;
  }
}
</style>
