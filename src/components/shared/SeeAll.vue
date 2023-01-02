<template>
  <span class="see-all">
    <RouterLink :to="route"> SEE ALL </RouterLink>
  </span>
</template>

<script setup lang="ts">
defineProps<{
  route: string;
}>();
</script>

<style lang="scss">
.see-all {
  font-size: $medium;
  opacity: 0.75;

  a:hover {
    cursor: pointer !important;
    text-decoration: underline;
  }
}
</style>
