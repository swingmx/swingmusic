<template>
  <div v-show="name == s.currentTab">
    <slot />
  </div>
</template>

<script setup lang="ts">
import useSearchStore from "@/stores/search";
const s = useSearchStore();
defineProps<{
  name: string;
}>();
</script>
