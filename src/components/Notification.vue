<template>
  <div
    class="new-notif rounded"
    :class="{ 'notif-error': notif.type == NotificationType.Error }"
    v-if="notif.visible"
  >
    <div>{{ notif.text }}</div>
  </div>
</template>

<script setup lang="ts">
import { useNotificationStore, NotificationType } from "../stores/notification";

const notif = useNotificationStore();
</script>
<style lang="scss">
.new-notif {
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

.notif-error {
  background-color: $red;
}
</style>
