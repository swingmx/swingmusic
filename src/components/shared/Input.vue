<template>
  <input
    type="search"
    class="header-input rounded-sm pad-sm"
    placeholder="search here"
    v-model.trim="source"
    id="page-search"
  />
</template>

<script setup lang="ts">
import usePStore from "@/stores/pages/playlist";
import { storeToRefs } from "pinia";
import { Routes } from "@/composables/enums";

const { query } = storeToRefs(usePStore());

const props = defineProps<{
  page: Routes;
}>();

function getRef() {
  switch (props.page) {
    case Routes.playlist:
      return query;

    case Routes.album:
      return query;

    default:
      return null;
  }
}

const source = getRef();
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
