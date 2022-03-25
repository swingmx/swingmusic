<template>
  <div class="new-notification rounded" v-if="store.visible">
    <div>{{ store.text }}</div>
  </div>
</template>

<script setup lang="ts">
import { useNotificationStore } from "../stores/notification";
const store = useNotificationStore();
</script>
<style lang="scss">
.new-notification {
  position: fixed;
  z-index: 2000;
  width: 25rem;
  bottom: 2rem;
  padding: $small;
  left: 50%;
  translate: -50%;
  background-color: rgb(5, 62, 168);
  display: grid;
  place-items: center;

  .link {
    font-weight: bold;
    text-decoration: underline;
  }
}
</style>
