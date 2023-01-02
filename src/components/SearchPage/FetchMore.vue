<template></template>
<script setup lang="ts">
import { onMounted } from "vue";

const props = defineProps<{
  action: () => void;
}>();

onMounted(() => {
  props.action();
});
</script>
