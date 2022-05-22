<template>
  <div v-show="name == selectedTab">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { inject } from "vue";

defineProps<{
  name: string;
}>();

const selectedTab = inject("currentTab");
</script>
