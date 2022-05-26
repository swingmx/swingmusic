<template>
  <div v-show="name == s.currentTab"  v-motion-slide-visible-top>
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
