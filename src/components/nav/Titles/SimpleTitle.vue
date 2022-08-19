<template>
  <div class="title">{{ text }}</div>
</template>

<script setup lang="ts">
defineProps<{
  text: string;
}>();
</script>
