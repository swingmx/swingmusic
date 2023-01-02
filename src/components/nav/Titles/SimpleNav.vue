<template>
  <h2 style="margin: 0">{{ text }}</h2>
</template>

<script setup lang="ts">
defineProps<{
  text: string;
}>();
</script>
