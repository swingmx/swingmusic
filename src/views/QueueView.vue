<template>
  <div class="queue-view">
    <Queue :isOnQueuePage="true" />
  </div>
</template>

<script setup lang="ts">
import Queue from "@/components/RightSideBar/Queue.vue";
</script>

<style lang="scss">
.queue-view {
  background-color: $black;
  height: 100%;
}
</style>
